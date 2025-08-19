## Como funciona 🔎

- Whisper → Transcreve o áudio e gera segmentos com timestamps.
- Pyannote → Detecta os locutores e seus intervalos de fala.

O script cruza os intervalos de tempo e atribui cada trecho ao locutor correto.
Exporta em um Word (.docx) organizado em colunas:

- Tempo
- Locutor
- Transcrição

---

## Funcionalidades

- Transcrição de áudio em texto usando **OpenAI Whisper**.
- Identificação de locutores usando **pyannote.audio** (diarização de fala).
- Exportação da transcrição em arquivo **Word (.docx)** organizado por tempo e locutor.

---

## Requisitos

- Python 3.10+  
- Bibliotecas Python:

```bash
pip install openai-whisper pyannote.audio python-docx

---

Token do Hugging Face (gratuito): necessário para usar o modelo de diarização pyannote/speaker-diarization.
Crie seu token em: https://huggingface.co/settings/tokens

## Como usar

Coloque o áudio que deseja transcrever na pasta do projeto (ex: exemplo.mp3).

