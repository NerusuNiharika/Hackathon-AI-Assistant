import streamlit as st

from langchain_qdrant import QdrantVectorStore
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from src.config import *


@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )


embeddings = load_embeddings()

# ============================================================
# QDRANT
# ============================================================

vector_store = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    embedding=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)


# ============================================================
# GROQ LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=GROQ_API_KEY,
    temperature=0
)


# ============================================================
# FINAL PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_template("""
Answer the question using the provided context.

Context:
{context}

Question:
{question}
""")


# ============================================================
# RAG
# ============================================================

def ask_rag(question):

    # Generate hypothetical answer
    hyde_prompt = f"""
    Write a detailed answer for:

    {question}
    """

    hypothetical_doc = llm.invoke(
        hyde_prompt
    )

    # Search using hypothetical answer
    docs = retriever.invoke(
        hypothetical_doc.content
    )

    # Combine retrieved context
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # Final answer
    final_prompt = prompt.format(
        context=context,
        question=question
    )

    response = llm.invoke(
        final_prompt
    )

    # Sources
    sources = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "N/A"
        )

        sources.append(
            f"{source} (Page {page})"
        )

    return {
        "answer": response.content,
        "sources": list(set(sources))
    }