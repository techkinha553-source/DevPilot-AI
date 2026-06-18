import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []

    def add(self, embedding, metadata):
        vector = np.array([embedding], dtype="float32")

        if self.index is None:
            dimension = vector.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(vector)
        self.metadata.append(metadata)

    def search(self, embedding, k=5):
        if self.index is None or len(self.metadata) == 0:
            return []

        query = np.array([embedding], dtype="float32")
        _, indices = self.index.search(query, k)

        results = []

        for idx in indices[0]:
            if 0 <= idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
    