from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from src.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    COLLECTION_NAME
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

# Project root = folder containing app.py
BASE_DIR = Path(__file__).resolve().parent.parent

PROBLEM_FOLDER = BASE_DIR / "data" / "problem_statements"
WINNING_FOLDER = BASE_DIR / "data" / "winning_projects"
URL_FILE = BASE_DIR / "data" / "urls" / "urls.txt"


# ============================================================
# 1. LOAD PROBLEM STATEMENT PDFs
# ============================================================

all_documents = []

print("\n--- Loading Problem Statements ---")

for pdf_file in PROBLEM_FOLDER.glob("*.pdf"):

    try:
        loader = PyPDFLoader(str(pdf_file))
        documents = loader.load()

        # Add category metadata
        for doc in documents:
            doc.metadata["document_type"] = "problem_statement"
            doc.metadata["file_name"] = pdf_file.name

        all_documents.extend(documents)

        print(f"Loaded: {pdf_file.name}")

    except Exception as e:
        print(f"Failed: {pdf_file.name}")
        print(e)


# ============================================================
# 2. LOAD WINNING PROJECT PDFs
# ============================================================

print("\n--- Loading Winning Projects ---")

for pdf_file in WINNING_FOLDER.glob("*.pdf"):

    try:
        loader = PyPDFLoader(str(pdf_file))
        documents = loader.load()

        # Add category metadata
        for doc in documents:
            doc.metadata["document_type"] = "winning_project"
            doc.metadata["file_name"] = pdf_file.name

        all_documents.extend(documents)

        print(f"Loaded: {pdf_file.name}")

    except Exception as e:
        print(f"Failed: {pdf_file.name}")
        print(e)


print(
    f"\nTotal PDF pages loaded: {len(all_documents)}"
)


# ============================================================
# 3. SPLIT PDF DOCUMENTS INTO CHUNKS
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(
    all_documents
)

print(
    f"Total PDF chunks created: {len(chunks)}"
)


# ============================================================
# 4. LOAD URLs
# ============================================================

print("\n--- Loading URLs ---")

all_url_docs = []

if URL_FILE.exists():

    with open(URL_FILE, "r", encoding="utf-8") as f:

        urls = [
            line.strip()
            for line in f
            if line.strip()
        ]

    print(f"URLs found: {len(urls)}")

else:

    print(f"URL file not found: {URL_FILE}")
    urls = []


# ============================================================
# 5. LOAD WEB PAGES
# ============================================================

for url in urls:

    try:

        loader = WebBaseLoader(url)

        docs = loader.load()

        for doc in docs:
            doc.metadata["document_type"] = "web_source"
            doc.metadata["source_url"] = url

        all_url_docs.extend(docs)

        print(f"Loaded: {url}")

    except Exception as e:

        print(f"Failed: {url}")
        print(e)


print(
    f"Total web documents loaded: {len(all_url_docs)}"
)


# ============================================================
# 6. SPLIT WEB DOCUMENTS
# ============================================================

url_chunks = text_splitter.split_documents(
    all_url_docs
)

print(
    f"Total URL chunks created: {len(url_chunks)}"
)


# ============================================================
# 7. COMBINE ALL CHUNKS
# ============================================================

all_chunks = chunks + url_chunks

print(
    f"\nTotal chunks to ingest: {len(all_chunks)}"
)


# ============================================================
# 8. CREATE EMBEDDINGS
# ============================================================

print("\n--- Loading Embedding Model ---")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# ============================================================
# 9. CONNECT TO QDRANT CLOUD
# ============================================================

print("\n--- Connecting to Qdrant ---")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=120
)

print("Connected to Qdrant")


# ============================================================
# 10. CREATE VECTOR STORE
# ============================================================

print(f"\n--- Using collection: {COLLECTION_NAME} ---")

vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings
)


# ============================================================
# 11. ADD DOCUMENTS IN BATCHES
# ============================================================

BATCH_SIZE = 50

total_chunks = len(all_chunks)

print(f"Total chunks to upload: {total_chunks}")
print(f"Batch size: {BATCH_SIZE}")

for start in range(0, total_chunks, BATCH_SIZE):

    end = min(start + BATCH_SIZE, total_chunks)

    batch = all_chunks[start:end]

    print(
        f"Uploading chunks {start + 1}-{end} "
        f"of {total_chunks}..."
    )

    vector_store.add_documents(batch)

    print(
        f"Completed: {end}/{total_chunks}"
    )


# ============================================================
# 12. VERIFY COLLECTION
# ============================================================

print("\n--- Verifying Qdrant collection ---")

collection_info = client.get_collection(
    COLLECTION_NAME
)

print(
    f"Collection points: "
    f"{collection_info.points_count}"
)


print("\n========================================")
print("INGESTION COMPLETED SUCCESSFULLY")
print("========================================")

print(f"Collection   : {COLLECTION_NAME}")
print(f"Total chunks : {total_chunks}")