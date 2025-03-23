# Import common utilities for easier access
from .call_llm import call_llm
from .errors import ValidationError, RateLimitError, APIError
from .validation import validate_llm_input, validate_embedding_input
from .web_search import search_web
from .get_embedding import get_embedding
from .vector_store import VectorStore
from .chunking import chunk_text
from .rate_limiter import RateLimiter, wait_for_rate_limit
from .async_utils import AsyncLLMClient, AsyncVectorStore, AsyncWebSearch

# Import stock analysis utilities
from .fetch_stock_data import fetch_stock_data, fetch_market_data
from .analyze_financials import analyze_stock_financials, compare_financials
from .analyze_sentiment import analyze_stock_sentiment

# Create a simple logger function
import logging

def get_logger(name):
    """Get a configured logger with the given name"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
