import os
import warnings
from dotenv import load_dotenv
import whisper
from pyannote.audio import Pipeline
from docx import Document

# -------------------------------
# 0. Supressão de warnings
# -------------------------------
warnings.filterwarnings("ignore")  # ignora warnings de torchaudio, PyTorch, etc.

# -------------------------------
# 1. Carregar variáveis de ambiente
# -------------------------------
load_dotenv()  # Carrega as variáveis do arquivo .env
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HUGGINGFACE_TOKEN:
    raise ValueError("❌ Token do HuggingFace não encontrado. Defina no arquivo .env")

# -------------------------------
# 2. Transcrição com Whisper
# -------------------------------
modelo = whisper.load_model("large")  # tiny, base, small, medium, large
audio_path = "exemplo.mp4"

print(">> Rodando Whisper...")
resultado = modelo.transcribe(audio_path)

# -------------------------------
# 3. Diarização com Pyannote
# -------------------------------
print(">> Rodando diarização...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=HUGGINGFACE_TOKEN
)

diarization = pipeline(audio_path)

# -------------------------------
# 4. Mesclar transcrição + locutores numerados
# -------------------------------
falas = []

# Dicionário para mapear locutores originais para "Locutor 1", "Locutor 2", ...
mapa_locutores = {}
contador_locutor = 1

for segmento in resultado["segments"]:
    start = segmento["start"]
    end = segmento["end"]
    texto = segmento["text"].strip()

    speaker = "Desconhecido"
    for turno in diarization.itertracks(yield_label=True):
        # Desempacotamento seguro independente da versão
        seg_dia = turno[0]        # primeiro elemento é sempre o segmento
        locutor_original = turno[-1]       # último elemento é o label/locutor
        s = seg_dia.start
        e = seg_dia.end
        if s <= start <= e:
            speaker = locutor_original
            break

    # Mapear locutor para "Locutor X"
    if speaker not in mapa_locutores and speaker != "Desconhecido":
        mapa_locutores[speaker] = f"Locutor {contador_locutor}"
        contador_locutor += 1

    nome_final = mapa_locutores.get(speaker, speaker)

    falas.append({
        "tempo": f"{start:.2f} - {end:.2f}",
        "locutor": nome_final,
        "texto": texto
    })

# -------------------------------
# 5. Exportar para Word
# -------------------------------
print(">> Exportando para Word...")
doc = Document()
doc.add_heading("Tabela 1 - transcrição de áudio ", level=1)

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
