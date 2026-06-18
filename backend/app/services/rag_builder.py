from app.services.embedding_service import create_embedding
from app.services.vector_store import VectorStore


def build_vector_store(documents):
    """
    Build a FAISS vector store from parsed documents.
    """
    store = VectorStore()

    for doc in documents:
        embedding = create_embedding(doc["content"])
        store.add(
            embedding=embedding,
            metadata={
                "path": doc["path"],
                "content": doc["content"],
            },
        )

    return store
