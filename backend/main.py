from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
import io

app = FastAPI()

# CORS (change origin after deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None


# Load ML model once
@app.on_event("startup")
def load_model():
    global model
    model = SentenceTransformer("all-MiniLM-L6-v2")


# Extract text from PDF
def extract_text(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text


# Extract email
def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else ""


# Extract phone
def extract_phone(text):
    match = re.search(r"\+?\d[\d -]{8,}\d", text)
    return match.group(0) if match else ""


# Calculate ATS score
def calculate_ats(resume, jd):
    embeddings = model.encode([resume, jd])
    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]
    return round(float(similarity) * 100, 2)


@app.get("/")
def home():
    return {"status": "API running"}


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        file_bytes = await resume.read()
        text = extract_text(file_bytes)

        if not text:
            return {"error": "Could not extract text from resume"}

        return {
            "ats_score": calculate_ats(text, job_description),
            "name": text.split("\n")[0],
            "email": extract_email(text),
            "phone": extract_phone(text),
        }

    except Exception as e:
        return {"error": str(e)}
