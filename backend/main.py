from fastapi import FastAPI, UploadFile, File, Form
import PyPDF2, re, nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware


nltk.download("punkt")
model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text(pdf):
    reader = PyPDF2.PdfReader(pdf)
    return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

def extract_email(text):
    m = re.search(r'\S+@\S+', text)
    return m.group() if m else ""

def extract_phone(text):
    m = re.search(r'\+?\d{10,13}', text)
    return m.group() if m else ""

def calculate_ats(resume, jd):
    v1 = model.encode([resume])
    v2 = model.encode([jd])
    return round(float(cosine_similarity(v1, v2)[0][0]) * 100, 2)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    content = await resume.read()
    with open("temp.pdf", "wb") as f:
        f.write(content)

    text = extract_text("temp.pdf")

    response = {
        "name": text.split("\n")[0],
        "email": extract_email(text),
        "phone": extract_phone(text),
        "ats_score": calculate_ats(text, job_description)
    }
    return response
