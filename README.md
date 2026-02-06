# 📄 Resume Analyzer & ATS Score Predictor

An AI-powered Resume Analyzer that calculates ATS match score using BERT embeddings and allows users to apply for jobs through an auto-filled application form.

## 🚀 Features
- Upload Resume PDF
- Paste Job Description
- Predict ATS Score using NLP + BERT
- Auto-fill candidate details
- Multi-step Job Application Portal
- Submit application with confirmation message

## 🛠 Tech Stack
- Frontend: React.js
- Backend: FastAPI (Python)
- AI Model: Sentence Transformers (BERT)
- NLP: NLTK, PyPDF2

## ▶ Run Project Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
