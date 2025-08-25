document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("video");
  const progressWrapper = document.getElementById("progress-wrapper");
  const progressBar = document.getElementById("progress");
  const percentText = document.getElementById("percent");

  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    let msg = document.getElementById("upload-success-msg");
    if (msg) msg.remove();

    const file = fileInput.files[0];
    if (!file) {
      alert("Escolha um arquivo primeiro");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    progressWrapper.style.display = "block";
    progressBar.value = 0;
    percentText.textContent = "0%";

    const xhr = new XMLHttpRequest();
    xhr.open("POST", form.action);

    xhr.upload.addEventListener("progress", function (evt) {
      if (evt.lengthComputable) {
        const percent = Math.round((evt.loaded / evt.total) * 100);
        progressBar.value = percent;
        percentText.textContent = percent + "%";
        if (percent === 100) {
          setTimeout(() => {
            progressWrapper.style.display = "none";
            showSuccessMessage();
            fileInput.value = ""; // Limpa o campo do vídeo
          }, 400);
        }
      }
    });

    xhr.onload = function () {
      if (xhr.status >= 200 && xhr.status < 300) {
        if (progressBar.value < 100) {
          progressBar.value = 100;
          percentText.textContent = "100%";
          setTimeout(() => {
            progressWrapper.style.display = "none";
            showSuccessMessage();
            fileInput.value = ""; // Limpa o campo do vídeo
          }, 400);
        }
      } else {
        alert("Upload falhou: " + xhr.statusText);
        progressWrapper.style.display = "none";
      }
    };

    xhr.onerror = function () {
      alert("Erro na requisição.");
      progressWrapper.style.display = "none";
    };

    xhr.send(formData);
  });

  function showSuccessMessage() {
    let msg = document.getElementById("upload-success-msg");
    if (msg) msg.remove();

    msg = document.createElement("div");
    msg.id = "upload-success-msg";
    msg.style.display = "flex";
    msg.style.alignItems = "center";
    msg.style.gap = "0.5em";
    msg.style.marginTop = "1.2rem";
    msg.style.fontWeight = "600";
    msg.style.color = "#2e7d32";
    msg.innerHTML =
      '<span style="font-size:1.5em;">&#10003;</span> Upload feito com sucesso!';
    form.parentNode.insertBefore(msg, form.nextSibling);
  }
});
