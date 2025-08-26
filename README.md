# Waiter

Um sistema de upload e streaming de vídeos com transcodificação automática e streaming adaptativo DASH.

## Introdução

Waiter é uma aplicação web que permite o upload de vídeos em diversos formatos (MP4. MOV, MKV, WebM e AVI), gera automaticamente múltiplas opções de resoluções (240p, 480p, 720p e 1080p) e fornece streaming adaptativo com qualidade automática baseada na conexão. 

## Tecnologias

O frontend foi desenvolvido sem o uso de frameworks, utilizando **HTML5** para a estruturação das páginas, **CSS3** para a estilização e **JavaScript ES6** para a manipulação do DOM, possibilitando a configuração de comportamentos dinâmicos no site. Para o streaming adaptativo, foi integrado o **dash.js**, player compatível com o protocolo DASH.

O backend foi implementado em **Flask**, framework web em **Python**, responsável pela criação dos endpoints da aplicação. Em conjunto, o **FFmpeg** foi utilizado para o processamento de áudio e vídeo, enquanto o **Pathlib** auxiliou na manipulação de caminhos de arquivos.

No processamento dos vídeos, foram adotados os codecs **H.264** (vídeo) e **AAC** (áudio), além do protocolo **DASH** para transmissão adaptativa.

## 📁 Estrutura do projeto

```
Waiter/
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

## Pré-requisitos

### Software Necessário
1. **Python 3.8** (ou superior)
2. **FFmpeg** (instalado e acessível via linha de comando)
3. **Git** (para clonagem do repositório)

### Instalação do FFmpeg

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
```

#### Windows:
1. Baixe o FFmpeg do [site oficial](https://ffmpeg.org/download.html)
2. Extraia e adicione ao PATH do sistema

## Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/1RodrigoSoares/Waiter.git
cd Waiter
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
pip install -r requirements.txt
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

## Como Usar

### 1. Upload de vídeo
1. Acesse a página principal
2. Clique no botão "Fazer upload".
3. Selecione um arquivo de vídeo e faça o envio
4. Aguarde até que o upload e o processamento seja feito

### 2. Assistir vídeos
1. Na página principal, veja a lista de vídeos
2. Vídeos prontos mostram "✓ Pronto para assistir"
3. Clique no vídeo para abrir o player
4. Use o dropdown para selecionar a qualidade ou deixe na automática (adaptativa)

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


## Melhorias Futuras

- [ ] Suporte a legendas
- [ ] Streaming ao vivo
- [ ] Compressão HEVC/H.265
- [ ] API REST completa
- [ ] Autenticação de usuários
- [ ] Análise de visualizações
- [ ] Suporte a playlists
- [ ] Integração com CDN

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autores

**Rodrigo Soares**
- GitHub: [@1RodrigoSoares](https://github.com/1RodrigoSoares)
- GitHub: [@lucasduartec](https://github.com/lucasduartec)
