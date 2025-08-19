import whisper
from pyannote.audio import Pipeline
from docx import Document

# -------------------------------
# 1. Transcrição com Whisper
# -------------------------------
modelo = whisper.load_model("small")  # pode ser tiny, base, small, medium, large
audio_path = "exemplo.mp3"

print(">> Rodando Whisper...")
resultado = modelo.transcribe(audio_path)

# -------------------------------
# 2. Diarização com Pyannote
# -------------------------------
print(">> Rodando diarização...")

# Use seu token do HuggingFace
HUGGINGFACE_TOKEN = "seu_token_aqui" #Coloque o TOKEN aqui

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=HUGGINGFACE_TOKEN
)

diarization = pipeline(audio_path)

# -------------------------------
# 3. Mesclar transcrição + locutores
# -------------------------------
falas = []

for segmento in resultado["segments"]:
    start = segmento["start"]
    end = segmento["end"]
    texto = segmento["text"].strip()

    # Achar o locutor pelo tempo
    speaker = "Desconhecido"
    for turno in diarization.itertracks(yield_label=True):
        (s, e), locutor = turno
        if s <= start <= e:
            speaker = locutor
            break

    falas.append({
        "tempo": f"{start:.2f} - {end:.2f}",
        "locutor": speaker,
        "texto": texto
    })

# -------------------------------
# 4. Exportar para Word
# -------------------------------
print(">> Exportando para Word...")
doc = Document()
doc.add_heading("Transcrição com Diarização", level=1)

tabela = doc.add_table(rows=1, cols=3)
hdr_cells = tabela.rows[0].cells
hdr_cells[0].text = 'Tempo'
hdr_cells[1].text = 'Locutor'
hdr_cells[2].text = 'Transcrição'

for fala in falas:
    row_cells = tabela.add_row().cells
    row_cells[0].text = fala["tempo"]
    row_cells[1].text = fala["locutor"]
    row_cells[2].text = fala["texto"]

doc.save("transcricao_diarizada.docx")
print("✅ Arquivo gerado: transcricao_diarizada.docx")
