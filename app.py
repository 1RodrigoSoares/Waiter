import os
import uuid
import shutil
import subprocess
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
from werkzeug.utils import secure_filename

# Configurações
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
VIDEOS_FOLDER = BASE_DIR / "videos"
ALLOWED_EXTENSIONS = {"mp4", "mov", "mkv", "webm", "avi"}

# Certifique-se que pastas existem
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
VIDEOS_FOLDER.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = "troque_esta_chave_para_producao"  # só para flashes (ex.: em dev)

# Helpers
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def run_command(cmd_list):
    """Roda um comando shell (lista) e lança exceção se falhar. Retorna (stdout, stderr)."""
    proc = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Comando falhou: {' '.join(cmd_list)}\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
    return proc.stdout, proc.stderr

def transcode_and_multiplex_dash(input_path: Path, dest_dir: Path):
    """
    Pipeline solicitado pelo usuário:
      - Gera três resoluções H.265: 1080p, 720p, 480p (sem áudio)
      - Gera duas faixas de áudio AAC: estéreo e mono
      - Multiplexa tudo em um único manifesto DASH (output.mpd) com segmentos .m4s
      - Gera uma thumbnail opcional (não interfere no DASH)
    """
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Arquivos intermediários
    v1080 = dest_dir / "video_1080p.mp4"
    v720  = dest_dir / "video_720p.mp4"
    v480  = dest_dir / "video_480p.mp4"
    a_st  = dest_dir / "audio_stereo.m4a"
    a_mo  = dest_dir / "audio_mono.m4a"
    mpd   = dest_dir / "output.mpd"
    thumb = dest_dir / "thumbnail.jpg"

    # Thumbnail (opcional)
    try:
        run_command([
            "ffmpeg", "-y",
            "-ss", "00:00:01",
            "-i", str(input_path),
            "-vframes", "1",
            "-q:v", "2",
            str(thumb)
        ])
    except Exception as e:
        print("Falha ao gerar thumbnail:", e)

    # Vídeo 1080p
    run_command([
        "ffmpeg", "-y", "-i", str(input_path),
        "-vf", "scale=1920:1080,setsar=1,setdar=16/9",
        "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-an",
        str(v1080)
    ])

    # Vídeo 720p
    run_command([
        "ffmpeg", "-y", "-i", str(input_path),
        "-vf", "scale=1280:720,setsar=1,setdar=16/9",
        "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-an",
        str(v720)
    ])

    # Vídeo 480p
    run_command([
        "ffmpeg", "-y", "-i", str(input_path),
        "-vf", "scale=854:480,setsar=1,setdar=16/9",
        "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-an",
        str(v480)
    ])

    # Áudio estéreo
    run_command([
        "ffmpeg", "-y", "-i", str(input_path),
        "-c:a", "aac", "-ac", "2", "-vn",
        str(a_st)
    ])

    # Áudio mono
    run_command([
        "ffmpeg", "-y", "-i", str(input_path),
        "-c:a", "aac", "-ac", "1", "-vn",
        str(a_mo)
    ])

    # Multiplexação DASH
    run_command([
        "ffmpeg",
        "-i", str(v1080),
        "-i", str(v720),
        "-i", str(v480),
        "-i", str(a_st),
        "-i", str(a_mo),
        "-map", "0:v", "-map", "1:v", "-map", "2:v",
        "-map", "3:a", "-map", "4:a",
        "-c", "copy",
        "-f", "dash",
        "-seg_duration", "4",
        "-use_timeline", "1",
        "-use_template", "1",
        "-adaptation_sets", "id=0,streams=0,1,2 id=1,streams=3,4",
        str(mpd)
    ])

    # Metadados simples
    (dest_dir / "meta.txt").write_text("original_filename={}\nmpd={}\n".format(input_path.name, mpd.name), encoding="utf-8")
    return mpd

# Rotas
@app.route("/")
def index():
    return redirect(url_for("list_videos"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "video" not in request.files:
            flash("Nenhum arquivo enviado", "danger")
            return redirect(request.url)
        file = request.files["video"]
        if file.filename == "":
            flash("Arquivo sem nome", "danger")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_id = uuid.uuid4().hex
            saved_name = f"{unique_id}_{filename}"
            save_path = UPLOAD_FOLDER / saved_name
            file.save(save_path)
            flash("Arquivo recebido. Processando (transcodificação + DASH)...", "info")

            video_dir = VIDEOS_FOLDER / unique_id
            try:
                mpd_path = transcode_and_multiplex_dash(save_path, video_dir)
                meta_path = video_dir / "meta.txt"
                if not meta_path.exists():
                    meta_path.write_text(f"original_filename={filename}\nmpd={mpd_path.name}\n", encoding="utf-8")
                flash("Processamento concluído!", "success")
            except Exception as e:
                if video_dir.exists():
                    shutil.rmtree(video_dir, ignore_errors=True)
                flash(f"Erro ao processar: {e}", "danger")
                return redirect(request.url)

            return redirect(url_for("list_videos"))
        else:
            flash("Extensão não permitida", "danger")
            return redirect(request.url)
    return render_template("upload.html")

@app.route("/videos")
def list_videos():
    videos = []
    for d in sorted(VIDEOS_FOLDER.iterdir(), key=os.path.getmtime, reverse=True):
        if not d.is_dir():
            continue
        video_id = d.name
        meta = {}
        meta_file = d / "meta.txt"
        if meta_file.exists():
            content = meta_file.read_text(encoding="utf-8")
            for line in content.splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    meta[k.strip()] = v.strip()
        videos.append({
            "id": video_id,
            "original_name": meta.get("original_filename", "Sem nome"),
            "thumbnail": f"/videos/{video_id}/thumbnail.jpg" if (d / "thumbnail.jpg").exists() else None,
            "mpd": meta.get("mpd", "output.mpd")
        })
    return render_template("list.html", videos=videos)

@app.route("/watch/<video_id>")
def watch(video_id):
    video_dir = VIDEOS_FOLDER / video_id
    if not video_dir.exists():
        flash("Vídeo não encontrado", "danger")
        return redirect(url_for("list_videos"))
    mpd_name = "output.mpd"
    meta_file = video_dir / "meta.txt"
    title = video_id
    if meta_file.exists():
        content = meta_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("mpd="):
                mpd_name = line.split("=",1)[1].strip()
            if line.startswith("original_filename="):
                title = line.split("=",1)[1].strip()
    mpd_url = url_for("serve_video_file", video_id=video_id, filename=mpd_name)
    return render_template("player.html", mpd_url=mpd_url, title=title, video_id=video_id)

@app.route("/videos/<video_id>/<path:filename>")
def serve_video_file(video_id, filename):
    safe_dir = VIDEOS_FOLDER / secure_filename(video_id)
    if not safe_dir.exists():
        return "Not found", 404
    return send_from_directory(safe_dir, filename)

# API helper para checar status (opcional)
@app.route("/api/video_status/<video_id>")
def video_status(video_id):
    d = VIDEOS_FOLDER / video_id
    return jsonify({
        "exists": d.exists(),
        "files": [f.name for f in d.iterdir()] if d.exists() else []
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
