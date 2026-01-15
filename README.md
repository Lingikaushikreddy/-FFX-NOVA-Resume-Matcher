# 🚀 FFX NOVA Resume Matcher

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![AI-Powered](https://img.shields.io/badge/AI-Powered-FF4B4B?style=for-the-badge)

**FFX NOVA Resume Matcher** is a next-generation hiring intelligence platform designed to replace legacy ATS with **Semantic Understanding**. 

Unlike traditional keyword scrapers, FFX NOVA uses **Hybrid AI** (Vector Embeddings + Weighted Keywords) to understand *context*, matching candidates to jobs based on their actual potential, not just their buzzwords.

---

## ✨ Features

### 📄 Intelligent Resume Parsing
- **Format Agnostic**: Extracts data perfectly from **PDF** and **DOCX**.
- **Deep Extraction**: Automatically captures:
    - 📞 Contact Info (Name, Email, Phone)
    - 🛠 Technical Skills (Programming, Tools, Frameworks etc.)
    - 💼 Work Experience (Timeline, Roles, Companies)
    - 🎓 Education
- **Soft Skill Detection**: Identifies leadership, communication, and management traits.

### 🧠 AI Matching Engine (Hybrid V1)
- **Semantic Core**: Uses `sentence-transformers` to map resumes and job descriptions into a 384-dimensional vector space.
- **Contextual Matching**: Understands that *"React Native"* is related to *"Mobile Dev"* even if the words don't match exactly.
- **Precision Keyword scoring**: Weighted filtering for hard requirements (e.g., "Must have Security Clearance").
- **Explainable AI (XAI)**: Don't just get a score. Get the **"WHY"**:
    > "87% Match: Strong semantic alignment in Backend Engineering, but missing specific 'AWS' certification."

### ⚡ Performance
- **FastAPI**: Asynchronous, high-performance API backend.
- **pgvector**: Native vector similarity search within PostgreSQL for million-scale scalability.

---

## 🛠️ Tech Stack

- **Core**: Python 3.10+
- **API Framework**: FastAPI
- **Database**: PostgreSQL 15+ (with `pgvector` extension)
- **AI/ML**: 
    - `sentence-transformers` (Embeddings)
    - `spacy` / `regex` (NER & Pattern Matching)
    - `scikit-learn` (Similarity Metrics)
- **Infrastructure**: Docker (planned)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL (with `pgvector` installed)

### 1. Clone the Repository
```bash
git clone https://github.com/Lingikaushikreddy/-FFX-NOVA-Resume-Matcher.git
cd -FFX-NOVA-Resume-Matcher
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Usage (CLI)
You can run the parser directly from the command line:

```bash
# Parse a resume and print JSON
python main.py parse-resume path/to/resume.pdf

# Parse a job description
python main.py parse-job path/to/job_desc.txt
```

### 4. Run the API Server
```bash
uvicorn api.app:app --reload
```
Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## 🗺️ Roadmap

- [x] Core Resume Parsing Pipeline (PDF/DOCX)
- [x] Skill & Experience Extraction
- [ ] **Phase 2: Matching Engine Implementation** (In Progress)
    - [ ] Vector Embedding Generation
    - [ ] Hybrid Scoring Algorithm
    - [ ] Match Result Persistence
- [ ] **Phase 3: Dashboard UI**
    - [ ] React/Next.js Frontend
    - [ ] Upload & Drag-and-Drop Interface

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
