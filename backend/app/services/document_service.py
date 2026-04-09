import fitz  # PyMuPDF
import re
import os

from app.services.embedding_service import get_embeddings
from app.db.faiss_manager import add_embeddings


# ==============================
# CONFIG
# ==============================

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


# ==============================
# EXTRACT TEXT PAGE-WISE
# ==============================

def extract_text_with_pages(file_path: str):
    doc = fitz.open(file_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()

        if not text or not text.strip():
            continue

        pages.append({
            "page": i,
            "text": text
        })

    return pages


# ==============================
# SEMANTIC CHUNKING
# ==============================

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()

        if current_length + len(words) > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            # overlap
            current_chunk = current_chunk[-overlap:] if overlap else []
            current_length = len(current_chunk)

        current_chunk.extend(words)
        current_length += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ==============================
# MAIN PIPELINE
# ==============================

def process_document(subject_id: str, doc_id: str, file_path: str):
    filename = os.path.basename(file_path)

    print(f"📄 Processing document: {filename}")

    pages = extract_text_with_pages(file_path)

    if not pages:
        print("❌ No text extracted from document")
        return

    valid_chunks = []
    metadata = []

    # 🔹 Build clean chunks + metadata
    for page_data in pages:
        page = page_data["page"]
        text = page_data["text"]

        chunks = chunk_text(text)

        for chunk in chunks:
            cleaned = chunk.strip()

            # 🔴 Filter bad chunks BEFORE embedding
            if not cleaned or len(cleaned) < 30:
                continue

            valid_chunks.append(cleaned)

            metadata.append({
                "doc_id": doc_id,
                "document_name": filename,
                "page": page + 1,
                "text": cleaned
            })

    # 🔴 Safety check
    if not valid_chunks:
        print("❌ No valid chunks generated")
        return

    print("Valid chunks:", len(valid_chunks))

    # 🔹 Generate embeddings
    embeddings = get_embeddings(valid_chunks)

    print("Embeddings:", len(embeddings))
    print("Metadata:", len(metadata))

    # 🔴 FINAL SAFETY FIX (guarantee match)
    min_len = min(len(metadata), embeddings.shape[0])

    if len(metadata) != embeddings.shape[0]:
        print("⚠️ Fixing mismatch automatically")

    metadata = metadata[:min_len]
    embeddings = embeddings[:min_len]

    # 🔹 Store in FAISS
    add_embeddings(subject_id, embeddings, metadata)

    print(f"✅ Successfully processed {min_len} chunks from {filename}")