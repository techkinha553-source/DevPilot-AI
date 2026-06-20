from app.services.chunker import chunk_text
from app.services.embedding_service import create_embedding
from app.services.vector_store import VectorStore


def build_vector_store(documents):
    """
    Build a vector store from parsed documents.
    """
    store = VectorStore()

    for document in documents:

        print(f"Processing {document['path']}")

        chunks = chunk_text(
            document["content"]
        )

        for index, chunk in enumerate(chunks):

            print(f"Chunk {index}")

            embedding = create_embedding(
                chunk
            )

            store.add(
                embedding,
                {
                    "path": document["path"],
                    "chunk": index,
                    "content": chunk
                }
            )

    return store
