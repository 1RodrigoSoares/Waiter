# VidTube - Sistema de Streaming de Vídeo com DASH

Um sistema completo de upload e streaming de vídeos com transcodificação automática e streaming adaptativo DASH (Dynamic Adaptive Streaming over HTTP).

## 🎯 Características

- **Upload de Vídeos**: Suporte para formatos MP4, MOV, MKV, WebM e AVI
- **Transcodificação Automática**: Geração automática de múltiplas resoluções (240p, 480p, 720p, 1080p)
- **Streaming DASH**: Streaming adaptativo com qualidade automática baseada na conexão
- **Interface Moderna**: Design responsivo e intuitivo
- **Controle de Qualidade**: Seleção manual de resolução via dropdown
- **Status de Processamento**: Indicadores visuais do progresso de transcodificação
- **Thumbnails Automáticas**: Geração automática de miniaturas dos vídeos

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **FFmpeg** - Processamento de vídeo e áudio
- **Pathlib** - Manipulação de caminhos de arquivos

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização responsiva
- **JavaScript ES6** - Interatividade
- **dash.js** - Player DASH para streaming adaptativo

### Processamento de Vídeo
- **H.264** - Codec de vídeo
- **AAC** - Codec de áudio
- **DASH** - Protocolo de streaming adaptativo

## 📋 Pré-requisitos

### Software Necessário
1. **Python 3.8 ou superior**
2. **FFmpeg** instalado e acessível via linha de comando
3. **Git** (para clonagem do repositório)

### Instalação do FFmpeg

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### CentOS/RHEL:
```bash
sudo yum install epel-release
sudo yum install ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
```

#### Windows:
1. Baixe o FFmpeg do [site oficial](https://ffmpeg.org/download.html)
2. Extraia e adicione ao PATH do sistema

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/1RodrigoSoares/VidTube.git
cd VidTube
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar Dependências
```bash
pip install flask werkzeug
```

### 4. Verificar FFmpeg
```bash
ffmpeg -version
```

### 5. Executar a Aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5001`

## 📁 Estrutura do Projeto

```
VidTube/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── static/               # Arquivos estáticos
│   ├── css/
│   └── js/
├── templates/            # Templates HTML
│   ├── base.html        # Template base
│   ├── list.html        # Lista de vídeos
│   ├── player.html      # Player de vídeo
│   └── upload.html      # Upload de vídeos
├── uploads/             # Vídeos enviados (temporário)
└── videos/              # Vídeos processados
    └── [video_id]/
        ├── output.mpd           # Manifesto DASH
        ├── thumbnail.jpg        # Miniatura
        ├── audio.m4a           # Áudio separado
        ├── chunk-stream*.m4s   # Segmentos de vídeo
        ├── init-stream*.m4s    # Segmentos de inicialização
        └── meta.txt            # Metadados
```

## 🎮 Como Usar

### 1. Upload de Vídeo
1. Acesse a página principal
2. Clique em "Enviar vídeo"
3. Selecione um arquivo de vídeo
4. Aguarde o processamento (indicado por spinner)

### 2. Assistir Vídeos
1. Na página principal, veja a lista de vídeos
2. Vídeos prontos mostram "✓ Pronto para assistir"
3. Clique no vídeo para abrir o player
4. Use o dropdown para selecionar a qualidade

### 3. Estados dos Vídeos
- **🔄 Processando**: Vídeo sendo transcodificado
- **✓ Pronto**: Disponível para reprodução
- **❌ Erro**: Falha no processamento

## ⚙️ Configurações

### Formatos Suportados
- MP4, MOV, MKV, WebM, AVI

### Resoluções Geradas
- **240p**: 426x240, CRF 28
- **480p**: 854x480, CRF 25
- **720p**: 1280x720, CRF 23
- **1080p**: 1920x1080, CRF 21

### Configurações de Áudio
- **Codec**: AAC
- **Taxa de bits**: 128k
- **Canais**: Estéreo

### Configurações DASH
- **Duração do segmento**: 3 segundos
- **Uso de timeline**: Habilitado
- **Adaptação automática**: Baseada na largura de banda

## 🔧 Personalização

### Alterar Qualidades de Vídeo
Edite a função `transcode_and_multiplex_dash` em `app.py`:

```python
# Exemplo: Adicionar resolução 4K
run_command([
    "ffmpeg", "-y", "-i", str(input_path),
    "-vf", "scale=3840:2160,setsar=1,setdar=16/9",
    "-c:v", "libx264", "-crf", "20", "-preset", "fast",
    "-an", str(v4k_dash)
])
```

### Modificar Interface
- **CSS**: Edite os estilos nos templates HTML
- **Layout**: Modifique os arquivos em `templates/`
- **JavaScript**: Personalize o player em `templates/player.html`

## 🐛 Solução de Problemas

### Erro: "FFmpeg não encontrado"
```bash
# Verificar se está instalado
which ffmpeg

# Instalar se necessário (Ubuntu)
sudo apt install ffmpeg
```

### Erro: "Comando falhou"
1. Verifique se o arquivo de vídeo não está corrompido
2. Confirme que há espaço em disco suficiente
3. Verifique as permissões das pastas `uploads/` e `videos/`

### Vídeo não carrega no player
1. Verifique se o processamento foi concluído
2. Confirme que o arquivo `.mpd` foi gerado
3. Verifique o console do navegador para erros JavaScript

### Performance lenta
1. Use um SSD para armazenamento
2. Aumente a RAM disponível
3. Configure preset FFmpeg mais rápido (ultrafast)

## 📈 Melhorias Futuras

- [ ] Suporte a legendas
- [ ] Streaming ao vivo
- [ ] Compressão HEVC/H.265
- [ ] API REST completa
- [ ] Autenticação de usuários
- [ ] Análise de visualizações
- [ ] Suporte a playlists
- [ ] Integração com CDN

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Rodrigo Soares**
- GitHub: [@1RodrigoSoares](https://github.com/1RodrigoSoares)

## 🙏 Agradecimentos

- [FFmpeg](https://ffmpeg.org/) - Processamento de mídia
- [dash.js](https://github.com/Dash-Industry-Forum/dash.js/) - Player DASH
- [Flask](https://flask.palletsprojects.com/) - Framework web Python

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
