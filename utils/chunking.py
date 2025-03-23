import re
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 100,
    split_on: Optional[str] = None
) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        split_on: Optional regex pattern to split on (e.g., '\n\n' for paragraphs)
    
    Returns:
        List of text chunks
    """
    logger.info(f"Chunking text of length {len(text)} with size={chunk_size}, overlap={overlap}")
    
    if split_on:
        # Split on pattern and recombine to respect chunk size
        pieces = re.split(split_on, text)
        chunks = []
        current_chunk = ""
        
        for piece in pieces:
            if len(current_chunk) + len(piece) > chunk_size:
                chunks.append(current_chunk)
                current_chunk = piece
            else:
                current_chunk += piece
        
        if current_chunk:
            chunks.append(current_chunk)
            
    else:
        # Simple character-based chunking with overlap
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
    
    logger.info(f"Created {len(chunks)} chunks")
    return chunks

if __name__ == "__main__":
    # Test the function
    text = "This is a test " * 100
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    print(f"Number of chunks: {len(chunks)}")
    print(f"First chunk: {chunks[0]}") 