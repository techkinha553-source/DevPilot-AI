from sentence_transformers import SentenceTransformer

# Load once when the server starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):
    """
    Create a local embedding for the given text.
    Returns a Python list of floats.
    """
    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return embedding.tolist()
