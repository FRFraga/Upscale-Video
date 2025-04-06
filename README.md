# 🖼️ Real-ESRGAN Video Upscaler com Áudio 🎥🎶

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![License](https://img.shields.io/github/license/seu-usuario/seu-repositorio)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2B-lightgrey)
![Status](https://img.shields.io/badge/Status-Estável-brightgreen)

Projeto para realizar **upscale de vídeos com Real-ESRGAN**, mantendo o **áudio original intacto** 🎧. O pipeline é otimizado com paralelismo automático para aproveitar ao máximo seu processador 💻.

---

## ✨ Funcionalidades

- 📹 Extração de frames via `ffmpeg`
- 🧠 Upscale com Real-ESRGAN (via NCNN Vulkan)
- 🔁 Benchmark automático para o melhor paralelismo
- 🗂️ Renomeação e ordenação dos frames
- 🎬 Compilação final com áudio original restaurado
- ⚡ Limpeza automática (só o `.mp4` final permanece)

---

## 🚀 Requisitos

### 🔧 Pré-requisitos

| Componente        | Versão mínima  | Instruções de Instalação                    |
|------------------|----------------|---------------------------------------------|
| Python           | 3.11+          | [Download Python](https://www.python.org/downloads/) |
| FFmpeg           | Qualquer recente | [Download FFmpeg](https://ffmpeg.org/download.html) |
| Real-ESRGAN NCNN  | v0.2.0 Windows | [Download Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases) |

> ⚠️ Certifique-se de que o Real-ESRGAN esteja extraído e o executável `.exe` acessível.

---

## 📦 Instalação das dependências

Instale os pacotes Python:

```bash
pip install tqdm
```

---

## 🛠️ Configuração do Script

No arquivo `upscale.py`, edite estas variáveis no início do código para refletirem seu ambiente:

```python
video_path = r"C:\CAMINHO\PARA\SEU\VIDEO.mp4"
realesrgan_path = r"C:\CAMINHO\PARA\realesrgan-ncnn-vulkan.exe"
```

---

## ▶️ Como executar

Basta rodar:

```bash
python upscale.py
```

O script irá:

1. Rodar um **benchmark automático**
2. Processar os frames com **paralelismo ideal**
3. Reconstruir o vídeo com **áudio original**
4. Salvar como `video_final.mp4` 🥳

> 📁 Todos os arquivos temporários são apagados automaticamente. Só o vídeo final permanece.

---

## 🧪 Testado em

- Windows 11 Pro 64-bit
- Python 3.11.9
- Real-ESRGAN NCNN v0.2.0 (Windows)
- FFmpeg versão 6.0

---

## ❤️ Créditos

- [xinntao/Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan)
- [FFmpeg](https://ffmpeg.org/)
- Projeto desenvolvido com suporte do ChatGPT 🤖

---

## 📸 Preview (antes/depois)

| Antes | Depois (IA) |
|-------|-------------|
| ![antes](https://imgur.com/r57HpWq.gif) | ![depois](https://imgur.com/cCFBYnN.gif) |

---

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.

---

## 🌐 Rodapé de orgulho

![GitHub repo size](https://img.shields.io/github/repo-size/seu-usuario/seu-repositorio)
![GitHub last commit](https://img.shields.io/github/last-commit/seu-usuario/seu-repositorio)
![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4-red)
