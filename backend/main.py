from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2, re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def load_model():
    global model
    model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

def calculate_ats(resume, jd):
    v1 = model.encode([resume])
    v2 = model.encode([jd])
    return round(float(cosine_similarity(v1, v2)[0][0]) * 100, 2)

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    content = await resume.read()
    text = extract_text(io.BytesIO(content))

    return {
        "ats_score": calculate_ats(text, job_description)
    }
