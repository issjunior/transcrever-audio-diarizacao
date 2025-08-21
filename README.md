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
```

---

## Como usar
### 1. Coloque o áudio que deseja transcrever na pasta do projeto (ex: exemplo.mp3).
### 2. Edite o arquivo Python com seu token Hugging Face:
```python
HUGGINGFACE_TOKEN = "seu_token_aqui"
```
#### O pipeline pyannote/speaker-diarization precisa de acesso autenticado ao Hugging Face.

### 3.Execute o script:
```bash
python transcrever.py
```
### 4. O resultado será exportado para transcricao_diarizada.docx.
---

## Saída esperada

```csharp
[00:00 - 00:12] Locutor 1: Bom dia, tudo bem?
[00:12 - 00:20] Locutor 2: Tudo sim, e você?
[00:20 - 00:25] Locutor 1: Também, obrigado.
```

