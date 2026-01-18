# 🚀 FFX NOVA Resume Matcher [v1.0]

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

**FFX NOVA Resume Matcher** is a next-generation hiring intelligence platform designed to replace legacy ATS with **Semantic Understanding**. 

Unlike traditional keyword scrapers, FFX NOVA uses **Hybrid AI** (Vector Embeddings + Weighted Keywords) to understand *context*, matching candidates to jobs based on their actual potential, not just their buzzwords.

---

## ✨ Features

### 💻 Modern Web Interface
- **Stunning Landing Page**: High-impact design with glassmorphism and smooth animations.
- **Drag & Drop Upload**: Intuitive resume upload zone with real-time feedback.
- **Job Results Dashboard**: Visual match scores (Semantic vs. Skill) and clearance level badges.
- **Responsive Design**: Built with **Tailwind CSS v4** for pixel-perfect mobile and desktop experiences.

### 🧠 AI Matching Engine (Hybrid V1)
- **Semantic Core**: Uses `sentence-transformers` to map resumes and job descriptions into a 384-dimensional vector space.
- **Precision Keyword Scoring**: Weighted filtering for hard requirements (e.g., "Must have Security Clearance").
- **Explainable AI (XAI)**: Provides detailed reasons for match scores (e.g., "Good skill overlap, but missing required security clearance").

### 📄 Intelligent Resume Parsing
- **Format Agnostic**: Extracts data perfectly from **PDF** and **DOCX**.
- **Deep Extraction**: Captures contact info, technical skills, work experience, and education.
- **Soft Skill Detection**: Identifies leadership, communication, and management traits.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 19 + Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Icons & UI**: Lucide React, Framer Motion

### Backend
- **API**: FastAPI (Async high-performance)
- **Database**: PostgreSQL 15+ (with `pgvector`)
- **AI/ML**: `sentence-transformers`, `spacy`, `scikit-learn`
- **Infrastructure**: Docker (planned)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- PostgreSQL (with `pgvector` installed)

### 1. Clone the Repository
```bash
git clone https://github.com/Lingikaushikreddy/-FFX-NOVA-Resume-Matcher.git
cd -FFX-NOVA-Resume-Matcher
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the API Server
uvicorn api.app:app --reload --port 8000
```
> API Docs available at: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
Open a new terminal window:
```bash
cd frontend

# Install Node dependencies
npm install

# Start the Development Server
npm run dev
```
> App running at: `http://localhost:5173`

---

## 🗺️ Roadmap

- [x] **Phase 1: Resume Parsing**
    - [x] PDF/DOCX Parsing Pipeline
    - [x] Skill & Experience Extraction

- [x] **Phase 2: Matching Engine**
    - [x] Vector Embedding Generation
    - [x] Hybrid Scoring Algorithm
    - [x] FastAPI Endpoints

- [x] **Phase 3: Frontend & Dashboard**
    - [x] Hero & Landing Page
    - [x] File Upload Interface
    - [x] Job Results UI with Glassmorphism
    - [x] Real-time API Integration Client
    - [x] Job Match Grid & Detail Modal
    - [x] Upskilling Recommendation Engine

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
