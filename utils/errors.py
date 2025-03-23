class LLMError(Exception):
    """Base class for LLM-related errors."""
    pass

class RateLimitError(LLMError):
    """Raised when rate limits are exceeded."""
    pass

class APIError(LLMError):
    """Raised when the API returns an error."""
    pass

class TokenLimitError(LLMError):
    """Raised when token limits are exceeded."""
    pass

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class EmbeddingError(Exception):
    """Base class for embedding-related errors."""
    pass

class VectorStoreError(Exception):
    """Base class for vector store related errors."""
    pass

class ChunkingError(Exception):
    """Base class for text chunking related errors."""
    pass

class WebSearchError(Exception):
    """Base class for web search related errors."""
    pass

class InputSafetyError(ValidationError):
    """Raised when input fails safety checks."""
    pass

class AsyncOperationError(Exception):
    """Raised when async operations fail."""
    pass 