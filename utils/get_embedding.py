import os
import google.generativeai as genai
import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

def get_embedding(text: str, model: str = "gemini-embedding-exp-03-07") -> List[float]:
    """
    Get embeddings for a piece of text using Google's Gemini API.
    
    Args:
        text: Text to embed
        model: Model name to use (default is experimental Gemini embedding model)
        
    Returns:
        List of floats representing the embedding vector
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
        
    genai.configure(api_key=api_key)
    logger.info(f"Getting embedding for text: {text[:50]}...")
    
    try:
        model = genai.GenerativeModel(model_name=model)
        embedding = model.embed_content(text)
        return embedding.values
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        raise

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

if __name__ == "__main__":
    # Test the function
    text = "Hello world"
    emb = get_embedding(text)
    print(f"Embedding dimension: {len(emb)}") 