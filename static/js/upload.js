// Este script substitui o envio de formulário padrão por uma requisição AJAX com progress bar.
document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("video");
  const progressWrapper = document.getElementById("progress-wrapper");
  const progressBar = document.getElementById("progress");
  const percentText = document.getElementById("percent");

  if (!form) return;

  form.addEventListener("submit", function(e) {
    e.preventDefault();
    const file = fileInput.files[0];
    if (!file) {
      alert("Escolha um arquivo primeiro");
      return;
    }

    const formData = new FormData();
    formData.append("video", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", form.action);

    xhr.upload.addEventListener("progress", function(evt) {
      if (evt.lengthComputable) {
        const percent = Math.round((evt.loaded / evt.total) * 100);
        progressWrapper.style.display = "block";
        progressBar.value = percent;
        percentText.textContent = percent + "%";
      }
    });

    xhr.onload = function() {
      if (xhr.status >= 200 && xhr.status < 300) {
        window.location.href = "/videos";
      } else {
        alert("Upload falhou: " + xhr.statusText);
      }
    };

    xhr.onerror = function() {
      alert("Erro na requisição.");
    };

    xhr.send(formData);
  });
});
