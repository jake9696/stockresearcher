import faiss
import numpy as np
from typing import List, Tuple
import logging
import pickle
import os

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, dimension: int = 1536):
        """Initialize a FAISS index for vector storage."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []  # Store original texts
        
    def add(self, embeddings: List[List[float]], texts: List[str]):
        """Add vectors and their corresponding texts to the store."""
        if not embeddings or not texts:
            return
            
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        self.texts.extend(texts)
        logger.info(f"Added {len(embeddings)} vectors to store")
        
    def search(self, query_vector: List[float], k: int = 5) -> List[Tuple[str, float]]:
        """Search for k nearest neighbors."""
        query_array = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_array, k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.texts):
                results.append((self.texts[idx], float(dist)))
                
        return results
        
    def save(self, path: str):
        """Save the index and texts to disk."""
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.texts", 'wb') as f:
            pickle.dump(self.texts, f)
            
    @classmethod
    def load(cls, path: str) -> 'VectorStore':
        """Load an index and texts from disk."""
        store = cls()
        store.index = faiss.read_index(f"{path}.index")
        with open(f"{path}.texts", 'rb') as f:
            store.texts = pickle.load(f)
        return store

if __name__ == "__main__":
    # Test the store
    store = VectorStore(dimension=3)
    vectors = [[1,0,0], [0,1,0], [0,0,1]]
    texts = ["doc1", "doc2", "doc3"]
    store.add(vectors, texts)
    
    query = [1,0,0]
    results = store.search(query, k=2)
    print("Search results:", results) 