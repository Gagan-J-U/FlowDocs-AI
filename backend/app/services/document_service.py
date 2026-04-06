from app.services.embedding_service import get_embeddings
from app.db.faiss_manager import add_embeddings
from app.services.document_service import extract_text_with_pages

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def extract_text_with_pages(file_path: str):
    doc = fitz.open(file_path)
    pages = []

    for i, page in enumerate(doc):
        pages.append({
            "page": i,
            "text": page.get_text()
        })

    return pages

def chunk_text(text):
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def process_document(subject_id: str, doc_id: str, file_path: str):
    pages = extract_text_with_pages(file_path)

    all_chunks = []
    metadata = []

    for page_data in pages:
        page = page_data["page"]
        text = page_data["text"]

        chunks = chunk_text(text)

        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({
                "doc_id": doc_id,
                "page": page,
                "text": chunk
            })

    embeddings = get_embeddings(all_chunks)

    # 🔥 append to FAISS (we will fix this next)
    add_embeddings(subject_id, embeddings, metadata)