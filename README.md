# 🚀 FlowDocs AI

> AI-powered document intelligence system with subject-based knowledge isolation, RAG, and hybrid LLM support.

---

## 🧠 Overview

FlowDocs AI is a **next-generation document interaction platform** that allows users to:

* 📂 Upload and manage documents
* 🧠 Organize them into structured **subjects**
* 💬 Chat with documents using AI (RAG)
* 🔍 Perform semantic search
* 🔐 Use **local AI models** for privacy

---

## 🎯 Key Idea

> Each **subject acts as an independent AI brain**

This ensures:

* No context mixing
* Better accuracy
* Clean organization
* Scalable architecture

---

## 🏗️ System Architecture

```
Frontend (React)
   ↓
Backend (FastAPI)
   ↓
----------------------------
| Core Services            |
|--------------------------|
| Workspace Service        |
| Subject Service          |
| Document Service         |
| Chat Service             |
| AI Service (RAG + LLM)   |
----------------------------
   ↓
Storage Layer
----------------------------
| PostgreSQL (metadata)    |
| FAISS (vector DB)        |
| File Storage             |
----------------------------
   ↓
LLM Layer
----------------------------
| Cloud (OpenAI)           |
| Local (Ollama)           |
----------------------------
```

---

## ⚙️ How It Works

### 📂 Document Processing

```
Upload → Extract Text → Chunk → Embeddings → Store (FAISS)
```

### 💬 Chat (RAG Mode)

```
Query → Retrieve Relevant Chunks → Add Chat History → LLM → Response
```

### 💬 General Chat

```
Query → LLM → Response
```

---

## 🧩 Core Features

* 📁 **Workspaces & Subjects**

  * Organize documents into structured environments

* 💬 **Chat with Documents**

  * Context-aware AI responses

* 🔍 **Semantic Search**

  * Find information by meaning, not keywords

* ⚡ **AI Actions**

  * Summarize, explain, extract key points

* 🔐 **Privacy Mode**

  * Switch to local LLM for sensitive data

---

## 🧠 Tech Stack

### Frontend

* React
* TypeScript
* Tailwind CSS
* Framer Motion
* Zustand

### Backend

* FastAPI (Python)
* SQLAlchemy
* JWT auth

### Database

* PostgreSQL

### Vector Database

* FAISS

### AI Layer

* OpenAI API (cloud)
* Ollama (local LLM)
* Gemini API

### Document Processing

* PyMuPDF / pdfplumber

---

## 📁 Backend Structure

```
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes/
│   │   └── deps.py
│   │
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── chat_service.py
│   │   └── document_service.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── db/
│   └── core/
```

---

## 🗄️ Database Design

* **Workspace**
* **Subject**
* **Document**
* **Chat**
* **Message**

Each subject maintains:

* Its own **vector database (FAISS)**
* Its own **chat history**

---

## 🔄 Data Flow

```
Frontend → Route → Schema → Service → Model → DB
                                    ↓
Frontend ← Schema ← Route ← Service
```

---

## 🔌 LLM Integration

FlowDocs supports **hybrid AI execution**:

* ☁️ Cloud Mode → OpenAI API
* 💻 Local Mode → Ollama

```
if subject.llm_mode == "cloud":
    use OpenAI
else:
    use local LLM
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-repo/flowdocs-ai.git
cd flowdocs-ai
```

---

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
alembic upgrade head
```

---

### 3. Run Backend

```bash
uvicorn main:app --reload
```

---

### 4. Setup FAISS Storage

```
storage/
└── subjects/
```

---

### 5. Frontend Setup

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

---

## API Surface

### Conversations

* `GET /conversations/workspace/{workspace_id}`
* `GET /conversations/{conversation_id}`
* `GET /conversations/{conversation_id}/messages`
* `DELETE /conversations/{conversation_id}`

### Streaming Chat

`POST /chat-stream/` is an authenticated Server-Sent Events endpoint. It emits `conversation`, `token`, `done`, and `error` events so the frontend can render partial tokens without full re-renders.

---

### 6. Environment Variables

Create `.env` file:

```
DATABASE_URL=postgresql://...
SECRET_KEY=...
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
OPENAI_API_KEY=...
GEMINI_API_KEY=...
GOOGLE_API_KEY=...
HF_LOCAL_FILES_ONLY=1
VITE_API_BASE_URL=http://localhost:8000
```

---

## Verification

```bash
cd backend
./venv/bin/python -m compileall app
./venv/bin/python -m pytest

cd ../frontend
npm run build
```

---

## 📌 MVP Scope

* Document upload
* Subject-based RAG
* Chat system
* Clean UI
* Cloud LLM

---

## 🧠 Future Enhancements

* Multi-user authentication
* Collaboration features
* Advanced workflows
* Cross-subject search
* Export summaries

---

## 💥 Why This Project Matters

FlowDocs AI combines:

* 🧠 AI + Knowledge Management
* ⚙️ Scalable Architecture
* 🔐 Privacy-first AI
* 📊 Real-world usability

---

## 📜 License

MIT License

---

## 👨‍💻 Built By

Team FlowDocs 🚀
