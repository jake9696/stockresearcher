import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from .errors import AsyncOperationError, APIError
from .validation import validate_llm_input, validate_embedding_input, validate_search_query
from .rate_limiter import rate_limiter, wait_for_rate_limit
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

class AsyncLLMClient:
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        if not self.google_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
            
        # Configure Google API
        genai.configure(api_key=self.google_key)
    
    async def call_llm(
        self,
        prompt: str,
        llm_type: str = "basic",
        use_cache: bool = True,
        max_retries: int = 3
    ) -> str:
        """Async version of LLM call."""
        # Validate input
        prompt = validate_llm_input(prompt)
        
        # Check rate limits
        if not wait_for_rate_limit("openrouter" if llm_type != "basic" else "gemini_basic"):
            raise AsyncOperationError("Rate limit exceeded and max retries reached")
        
        # Select model
        if llm_type in ["thinking", "code", "creative", "math"]:
            model = "anthropic/claude-3-sonnet:thinking"
        else:
            model = "google/gemini-2.0-flash-exp:free"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openrouter_key}",
                        "HTTP-Referer": "https://github.com/your-repo",
                        "X-Title": "Stock Researcher"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 500000,
                        "temperature": 0.7 if llm_type == "creative" else 0.2
                    }
                ) as response:
                    if response.status != 200:
                        raise APIError(f"API returned status {response.status}")
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                    
        except Exception as e:
            logger.error(f"Async LLM call failed: {str(e)}")
            raise AsyncOperationError(f"LLM call failed: {str(e)}")

    async def get_embedding(self, text: str) -> List[float]:
        """Async version of embedding generation."""
        # Validate input
        text = validate_embedding_input(text)
        
        # Check rate limits
        if not wait_for_rate_limit("gemini_embedding"):
            raise AsyncOperationError("Embedding rate limit exceeded")
            
        try:
            model = genai.GenerativeModel("gemini-embedding-exp-03-07")
            embedding = await asyncio.to_thread(model.embed_content, text)
            return embedding.values
        except Exception as e:
            logger.error(f"Async embedding generation failed: {str(e)}")
            raise AsyncOperationError(f"Embedding generation failed: {str(e)}")

class AsyncVectorStore:
    """Async wrapper around our vector store operations."""
    def __init__(self, dimension: int = 1536):
        from .vector_store import VectorStore
        self.store = VectorStore(dimension)
    
    async def add(self, embeddings: List[List[float]], texts: List[str]):
        """Async version of vector store add operation."""
        await asyncio.to_thread(self.store.add, embeddings, texts)
    
    async def search(self, query_vector: List[float], k: int = 5):
        """Async version of vector store search operation."""
        return await asyncio.to_thread(self.store.search, query_vector, k)
    
    async def save(self, path: str):
        """Async version of vector store save operation."""
        await asyncio.to_thread(self.store.save, path)
    
    @classmethod
    async def load(cls, path: str):
        """Async version of vector store load operation."""
        instance = cls()
        instance.store = await asyncio.to_thread(instance.store.load, path)
        return instance

class AsyncWebSearch:
    """Async version of web search operations."""
    def __init__(self):
        self.api_key = os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY environment variable not set")
    
    async def search(
        self,
        query: str,
        max_results: int = 5
    ) -> List[Dict[str, str]]:
        """Async version of web search."""
        # Validate input
        query = validate_search_query(query)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers={
                        "Accept": "application/json",
                        "X-Subscription-Token": self.api_key
                    },
                    params={
                        "q": query,
                        "count": max_results
                    }
                ) as response:
                    if response.status != 200:
                        raise APIError(f"Brave Search API returned status {response.status}")
                    
                    data = await response.json()
                    results = []
                    for item in data.get("web", {}).get("results", []):
                        results.append({
                            "title": item.get("title"),
                            "url": item.get("url"),
                            "snippet": item.get("description")
                        })
                    
                    return results
                    
        except Exception as e:
            logger.error(f"Async web search failed: {str(e)}")
            raise AsyncOperationError(f"Web search failed: {str(e)}")

# Create global instances
async_llm = AsyncLLMClient()
async_web_search = AsyncWebSearch()

if __name__ == "__main__":
    async def test():
        # Test LLM
        response = await async_llm.call_llm("What is 2+2?", llm_type="basic")
        print("LLM Response:", response)
        
        # Test embedding
        emb = await async_llm.get_embedding("Hello world")
        print("Embedding dimension:", len(emb))
        
        # Test web search
        results = await async_web_search.search("Python programming")
        print("Search results:", results)
    
    asyncio.run(test()) 