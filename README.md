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
# FlowDocs AI

Tagline: A subject-aware collaborative research workspace — document ingestion, hybrid retrieval (FAISS + BM25), configurable LLMs, and real-time collaboration.

---

## Overview

FlowDocs AI is a research-focused collaborative platform that helps teams ingest documents (PDFs), extract and index content, and interact with those documents via a conversational AI assistant. It isolates knowledge by subject and workspace, supports real-time team collaboration (workspace chat and DMs), and provides a hybrid retrieval pipeline combining dense embeddings (FAISS) and sparse retrieval (BM25) with optional cross-encoder reranking.

Why it exists
- Turn collections of PDFs and figures into searchable knowledge bases scoped by workspace and subject.
- Provide a provider-agnostic AI layer (local + cloud) so teams can balance privacy and capability.

Problem it solves
- Makes internal documents and research discoverable, queryable, and collaboratively reviewable using a chat-first interface.

---

## Key Innovations

### Subject-Isolated Retrieval Architecture
- Each subject keeps its own FAISS index and BM25 corpus on-disk, preventing cross-subject leakage and making incremental reindexing efficient.
- Implementation: [backend/main.py](backend/main.py#L1-L200), [backend/app/vectorstore/faiss_service.py](backend/app/vectorstore/faiss_service.py#L1-L260)

### Collaborative AI Workspaces
- Role-based workspaces with owner/editor/viewer roles; workspace-scoped subjects and documents with access checks enforced in services.
- Implementation: [backend/app/models/workspace.py](backend/app/models/workspace.py#L1-L120), [backend/app/services/workspace_access_service.py](backend/app/services/workspace_access_service.py#L1-L200)

### Hybrid Local + Cloud AI
- Local embedding generation (sentence-transformers) + FAISS storage; LLM provider adapters for Ollama (local), OpenAI, and Gemini.
- Implementation: [backend/app/embeddings/embedding_service.py](backend/app/embeddings/embedding_service.py#L1-L140), [backend/app/llm/factory.py](backend/app/llm/factory.py#L1-L60)

### Researcher Discovery
- Per-user research profiles and semantic discovery endpoints for collaborator matching.
- Implementation: [backend/app/models/research_profile.py](backend/app/models/research_profile.py#L1-L120), [backend/app/api/routes/research.py](backend/app/api/routes/research.py#L1-L200)

### Real-Time Collaboration
- WebSocket-based workspace chat, DMs, presence, and notifications with a connection manager that broadcasts messages to active sockets.
- Implementation: [backend/app/api/routes/websockets.py](backend/app/api/routes/websockets.py#L1-L260), [backend/app/websocket/connection_manager.py](backend/app/websocket/connection_manager.py#L1-L200)

### Metadata-Aware Retrieval
- Chunks preserve section titles, parent section, hierarchy levels and page ranges for richer citation and context in prompts.
- Implementation: [backend/app/models/chunk.py](backend/app/models/chunk.py#L1-L120)

### Advanced Reasoning Modes
- Multiple prompt strategies (teaching, debate, researcher, expert, etc.) are implemented to adapt LLM behavior.
- Implementation: [backend/app/prompting/strategies](backend/app/prompting/strategies)

---

## Features

### Implemented Features
- User authentication (register/login) with JWT-based tokens ([backend/app/api/routes/auth.py](backend/app/api/routes/auth.py#L1-L160)).
- Workspaces, subjects, documents, and chunk storage via SQLAlchemy models ([backend/app/models](backend/app/models)).
- Document upload endpoint that triggers an asynchronous ingestion pipeline (PDF extraction → section detection → chunking → filtering → DB storage → embeddings → FAISS & BM25 indexing → figure indexing): [backend/app/services/document_ingestion_service.py](backend/app/services/document_ingestion_service.py#L1-L400).
- Local embedding generation using sentence-transformers and FAISS-based vector storage per subject: [backend/app/embeddings/embedding_service.py](backend/app/embeddings/embedding_service.py#L1-L140), [backend/app/vectorstore/faiss_service.py](backend/app/vectorstore/faiss_service.py#L1-L260).
- Hybrid retrieval pipeline (FAISS dense + BM25 sparse) with optional cross-encoder reranking: [backend/app/rag/retriever.py](backend/app/rag/retriever.py#L1-L340), [backend/app/rag/reranker.py](backend/app/rag/reranker.py#L1-L120).
- Chat orchestration with RAG and general pipelines: [backend/app/chat/pipelines/rag_pipeline.py](backend/app/chat/pipelines/rag_pipeline.py#L1-L200), [backend/app/chat/pipelines/general_pipeline.py](backend/app/chat/pipelines/general_pipeline.py#L1-L120).
- Figure extraction and indexing (captions + image FAISS indexes): [backend/app/services/figure_service.py] and [backend/app/vectorstore/figure_image_faiss.py].
- WebSocket-based workspace chat and direct messaging with presence and notifications: [backend/app/api/routes/websockets.py](backend/app/api/routes/websockets.py#L1-L260), frontend WebSocket client: [frontend/src/lib/websocket.ts](frontend/src/lib/websocket.ts#L1-L200).
- Research profile CRUD and discovery endpoints: [backend/app/api/routes/research.py](backend/app/api/routes/research.py#L1-L200).

### Partial / In-Progress Features
- Figure image indexing exists but may require specialized image embedding model for production-quality image search (implementation is present but may need tuning).
- Presence, notifications, and frontend UX are functional, but polishing and robustness improvements would be beneficial (some duplicated methods in the connection manager indicate cleanup opportunities).

### Planned Features (not invented)
- The codebase contains no explicit TODO roadmap entries; deployment automation (Docker/compose) and background worker orchestration (e.g., Celery) are not present in the repository.

---

## System Architecture

High-level text diagram

- Frontend (React/Vite) ↔ Backend (FastAPI) ↔ Database (Postgres via SQLAlchemy / Alembic)
- Backend: ingestion workers (background tasks), FAISS vector store (local files per subject), BM25 corpora (pickled), figure image indexes, LLM provider adapters
- Realtime: WebSocket connection manager for workspace chat, DMs, and notifications

Mermaid: High-level architecture

```mermaid
flowchart TD
  subgraph FE[Frontend]
    A[React App (Vite/Tailwind)] -->|REST / WebSocket| B[Backend API + WS]
  end

  subgraph BE[Backend]
    B --> C[Auth & Users]
    B --> D[Ingestion Pipeline]
    B --> E[Retrieval Layer]
    B --> F[LLM Providers]
    B --> G[Notifications / Presence]
  end

  subgraph DB[Database]
    C --> DB[(Postgres via SQLAlchemy)]
    D --> DB
    E --> DB
  end

  subgraph VS[Vector Storage]
    E --> FAISS[(FAISS index files)]
    E --> BM25[(pickled BM25 corpus)]
  end

  F -->|streams| LLM[Ollama / OpenAI / Gemini]
  G --> WS[WebSocket clients]
```

Retrieval flow

```mermaid
flowchart TD
  Q[User Query] --> Embed[Query Embedding (sentence-transformers)]
  Embed --> FAISS[FAISS Search (per subject)]
  Q --> BM25[BM25 Sparse Search]
  FAISS --> Merge[Merge Dense & Sparse]
  Merge --> Rerank{Use Reranker?}
  Rerank -->|yes| CrossEncoder[CrossEncoder Rerank]
  Rerank -->|no| TopK[Select Top K]
  TopK --> BuildPrompt[Prompt Strategy + Source Citations]
  BuildPrompt --> LLM
  LLM --> Answer[Assistant Answer + Citations]
```

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend framework | FastAPI | HTTP + WebSocket API |
| ASGI server | Uvicorn | Running FastAPI in development |
| ORM / Migrations | SQLAlchemy / Alembic | DB models and schema migrations |
| Database | Postgres (via DATABASE_URL) | Primary persistent storage |
| Embeddings | sentence-transformers | Local embedding model (configurable) |
| Vector DB | FAISS (faiss-cpu) | Dense vector index per subject |
| Sparse retriever | rank-bm25 | BM25 index for lexical retrieval |
| Reranker | CrossEncoder (sentence-transformers) | Cross-encoder reranking |
| PDF processing | PyMuPDF, pdfplumber | PDF text and figure extraction |
| LLM Providers | Ollama, OpenAI, Gemini | Model abstraction and streaming |
| Frontend | React, Vite, TypeScript, TailwindCSS | UI client |
| Real-time | WebSockets (FastAPI) | Workspace chat & DMs |
| Auth | OAuth2 password flow, python-jose, passlib/bcrypt | JWT auth + password hashing |

---

## Project Structure

Top-level (abridged)

```
FlowDocs-AI/
├─ backend/
│  └─ app/
│     ├─ api/routes/  # FastAPI routes
│     ├─ chat/        # Orchestration & pipelines
│     ├─ rag/         # Retrieval components
│     ├─ embeddings/  # Embedding model wrapper
│     ├─ vectorstore/ # FAISS helpers
│     ├─ ingestion/   # PDF extraction, chunking
│     ├─ llm/         # Provider adapters
++│     └─ models/      # SQLAlchemy models
├─ frontend/
│  └─ src/            # React app
└─ README.md
```

Folder responsibilities
- `backend/app/api/routes` — controllers exposing REST + WS endpoints (auth, chat, documents, research, dm, websockets).
- `backend/app/ingestion` — PDF extraction, section detection, chunking, filtering.
- `backend/app/rag` — retrieval glue code (bm25, faiss, hybrid merge, reranking).
- `backend/app/llm` — provider-agnostic LLM adapters.
- `frontend/src` — UI, including `frontend/src/lib/websocket.ts` (WebSocket helper).

Important files
- [backend/main.py](backend/main.py#L1-L200)
- [backend/app/services/document_ingestion_service.py](backend/app/services/document_ingestion_service.py#L1-L400)
- [backend/app/embeddings/embedding_service.py](backend/app/embeddings/embedding_service.py#L1-L140)
- [backend/app/vectorstore/faiss_service.py](backend/app/vectorstore/faiss_service.py#L1-L260)
- [frontend/src/lib/websocket.ts](frontend/src/lib/websocket.ts#L1-L200)

---

## Database Design

Key entities
- `users` — id, username, email, hashed_password, is_active, created_at ([backend/app/models/user.py](backend/app/models/user.py#L1-L140))
- `workspaces` — id, name, user_id (owner), created_at ([backend/app/models/workspace.py](backend/app/models/workspace.py#L1-L120))
- `workspace_members` — user_id, workspace_id, role
- `subjects` — id, name, workspace_id ([backend/app/models/subject.py](backend/app/models/subject.py#L1-L120))
- `documents` — filename, stored_filename, file_path, subject_id, processing_status ([backend/app/models/document.py](backend/app/models/document.py#L1-L200))
- `chunks` — document_id, chunk_index, text, section metadata ([backend/app/models/chunk.py](backend/app/models/chunk.py#L1-L120))
- `conversations` / `messages` — conversation history; `dm_conversation` / `dm_message` / `dm_participant` for direct messages
- `research_profiles` — per-user researcher metadata ([backend/app/models/research_profile.py](backend/app/models/research_profile.py#L1-L120))

ER diagram

```mermaid
erDiagram
  USERS ||--o{ WORKSPACES : owns
  WORKSPACES ||--o{ SUBJECTS : contains
  SUBJECTS ||--o{ DOCUMENTS : contains
  DOCUMENTS ||--o{ CHUNKS : contains
  WORKSPACES ||--o{ WORKSPACE_MEMBERS : has
  USERS ||--o{ WORKSPACE_MEMBERS : member_of
  CONVERSATIONS ||--o{ MESSAGES : contains
  USERS ||--o{ MESSAGES : sends
  DM_CONVERSATIONS ||--o{ DM_MESSAGES : contains
  USERS ||--o{ DM_PARTICIPANTS : participates
```

---

## Authentication & Security

Implemented
- Registration and login endpoints with password hashing via `passlib`/bcrypt and JWT creation/validation in [backend/app/core/security.py](backend/app/core/security.py#L1-L160).
- REST auth dependency: `get_current_user` and WebSocket JWT extractor `get_current_user_ws` in [backend/app/api/dependencies/auth.py](backend/app/api/dependencies/auth.py#L1-L200).

Authorization
- Workspace access and role verification enforced by `verify_workspace_access` and `verify_workspace_role` in [backend/app/services/workspace_access_service.py](backend/app/services/workspace_access_service.py#L1-L200).

Environment variables used for security:
- `AUTH_SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`

---

## Document Processing Pipeline

Step-by-step (implemented)
1. Upload: `POST /documents/upload/{subject_id}` saves file to `uploads/subject_id/` and creates a Document row. ([backend/app/api/routes/document.py](backend/app/api/routes/document.py#L1-L200)).
2. Background ingestion: `ingest_document_by_id` runs as a background task performing extraction → sections → chunking → filtering → store → embeddings → indexing. See [backend/app/services/document_ingestion_service.py](backend/app/services/document_ingestion_service.py#L1-L400).
3. After ingestion, document status changes (`processing` → `ready` or `error_*`).

Mermaid pipeline

```mermaid
flowchart TD
  Upload[Upload PDF] --> Extract[Extract pages & images]
  Extract --> Sections[Section detection & TOC]
  Sections --> Chunk[Chunking]
  Chunk --> Filter[Filter chunks]
  Filter --> StoreDB[Store chunks in DB]
  StoreDB --> Emb[Generate embeddings]
  Emb --> FAISS[Add embeddings to FAISS]
  StoreDB --> BM25[Save BM25 corpus]
  Extract --> Figures[Store & index figures]
  FAISS --> Ready[Document processing complete]
```

---

## Retrieval Architecture

Explained components
- Embeddings: Local SentenceTransformer model (configurable via `EMBEDDING_MODEL`) producing normalized float32 vectors. ([backend/app/embeddings/embedding_service.py](backend/app/embeddings/embedding_service.py#L1-L140)).
- Dense search: FAISS IndexFlatIP per subject; chunk id mapping stored as pickle files per subject. ([backend/app/vectorstore/faiss_service.py](backend/app/vectorstore/faiss_service.py#L1-L260)).
- Sparse search: BM25 corpus persisted as pickled files per subject and loaded into a cached BM25 index.
- Hybrid merging: dense + sparse merged and re-ranked; optional reranker uses CrossEncoder for higher precision. ([backend/app/rag/retriever.py](backend/app/rag/retriever.py#L1-L340), [backend/app/rag/reranker.py](backend/app/rag/reranker.py#L1-L120)).

Implementation detail
- `retrieve_chunks` produces query embedding → FAISS search → BM25 search → merge → optional rerank → top-K results for prompt building.

---

## AI Layer

Provider abstraction
- `get_llm_provider` returns `OllamaProvider`, `OpenAIProvider`, or `GeminiProvider` based on config. ([backend/app/llm/factory.py](backend/app/llm/factory.py#L1-L60)).

Adapters
- `OllamaProvider` — local Ollama chat client, streaming supported. ([backend/app/llm/providers/ollama_provider.py](backend/app/llm/providers/ollama_provider.py#L1-L120)).
- `OpenAIProvider` — OpenAI chat completions with streaming. ([backend/app/llm/providers/openai_provider.py](backend/app/llm/providers/openai_provider.py#L1-L120)).
- `GeminiProvider` — Google GenAI wrapper. ([backend/app/llm/providers/gemini_provider.py](backend/app/llm/providers/gemini_provider.py#L1-L220)).

---

## Collaboration Architecture

Implemented
- Workspaces and workspace membership with role-based checks.
- Workspace chat and DMs persisted and broadcast via WebSockets; presence and notification channels supported.

Files
- [backend/app/api/routes/websockets.py](backend/app/api/routes/websockets.py#L1-L260)
- [backend/app/websocket/connection_manager.py](backend/app/websocket/connection_manager.py#L1-L200)

---

## Research Networking

Implemented
- Research profiles and discovery endpoints that return semantic matches: [backend/app/api/routes/research.py](backend/app/api/routes/research.py#L1-L200)

---

## API Documentation (selected endpoints)

| Method | Endpoint | Purpose |
|---:|---|---|
| POST | /auth/register | Create new user |
| POST | /auth/login | Login (OAuth2 password flow) → returns `access_token` |
| POST | /chat/ | Generate chat response (RAG or general) |
| POST | /chat/stream | Streaming chat endpoint |
| POST | /documents/upload/{subject_id} | Upload PDF and start ingestion |
| GET | /documents/subject/{subject_id} | List documents for a subject |
| POST | /dm/conversations | Create DM conversation |
| GET | /dm/conversations | List DM conversations |
| GET | /dm/conversations/{id}/messages | List DM messages |
| POST | /dm/conversations/{id}/messages | Send DM message |
| GET | /conversations/workspace/{workspace_id} | List conversations in workspace |
| GET | /conversations/{id} | Get conversation details |
| POST | /conversations/{id}/share | Share conversation |
| POST | /conversations/{id}/private | Make conversation private |
| GET | /research/discover | Discover researchers (query) |
| PUT | /research/profile | Upsert user research profile |
| WS | /ws/workspaces/{workspace_id}?token=... | Workspace chat WebSocket |
| WS | /ws/dm/{conversation_id}?token=... | DM WebSocket |

---

## Installation

### Backend Setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r backend/requirements.txt
```

Env vars (example):
```
DATABASE_URL=postgresql://user:pass@localhost:5432/flowdocs
AUTH_SECRET_KEY=replace_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
HF_LOCAL_FILES_ONLY=1
OPENAI_API_KEY=
GEMINI_API_KEY=
CORS_ORIGINS=http://localhost:5173
```

Run migrations:
```
cd backend
alembic upgrade head
```

Start server:
```
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```
cd frontend
npm install
npm run dev
```

---

## Usage Walkthrough

1. Register user: `POST /auth/register`.
2. Login: `POST /auth/login` → get bearer token.
3. Create workspace and subject.
4. Upload PDF: `POST /documents/upload/{subject_id}`.
5. Wait for ingestion to complete (`processing_status` → `ready`).
6. Chat via `POST /chat/` with `chat_type=rag`.
7. Use WebSockets for real-time chat: `/ws/workspaces/{workspace_id}` or `/ws/dm/{conversation_id}`.

---

## Screenshots

Add screenshots under `frontend/public/screenshots/` for: workspace list, document upload, chat with citations, workspace chat.

---

## Performance Considerations

- Subject isolation reduces vector store size per index and improves retrieval latency.
- FAISS `IndexFlatIP` is appropriate for modest datasets; migrate to IVF/PQ for large-scale use.
- BM25 corpus is cached in memory via `bm25_cache` to reduce disk I/O.
- Cross-encoder reranker is expensive — limit to top-N candidates.

---

## Roadmap

### Current Stage
- Implemented: ingestion pipeline, hybrid retrieval, reranker, provider adapters, real-time chat, research discovery.

### Next Milestones
- Add Dockerfiles and `docker-compose.yml` for dev/production.
- Move ingestion to background worker (Celery/RQ).
- Add CI for linting and tests.

---

## Contributing

- Fork, create a feature branch, and open PRs.
- Run formatting (black/isort) and tests before submitting PR.

---

## License

MIT License (placeholder) — add `LICENSE` file to assert final terms.

---

## Maintainer Notes

- No Dockerfile/docker-compose present — deployment manifests missing.
- In-process BackgroundTasks are used for ingestion; consider an external worker for scale.
- `backend/app/websocket/connection_manager.py` has duplicate methods and debug prints; refactor for clarity.

If you want, I can scaffold Docker/dev compose and a basic GitHub Actions CI next.
