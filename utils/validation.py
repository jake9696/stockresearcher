import re
from typing import Optional, List, Dict, Any
import logging
from .errors import ValidationError, InputSafetyError

logger = logging.getLogger(__name__)

class InputValidator:
    # Common patterns for validation
    PATTERNS = {
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "url": r"^https?:\/\/[\w\-]+(\.[\w\-]+)+[/#?]?.*$",
        "phone": r"^\+?[\d\-\(\) ]{8,}$"
    }
    
    # Content moderation keywords (basic example - expand as needed)
    UNSAFE_PATTERNS = [
        r"(?i)(hack|exploit|vulnerability|inject)",
        r"(?i)(private.*key|secret.*key|password)",
        r"(?i)(social security|credit card)",
    ]
    
    @staticmethod
    def validate_length(text: str, max_length: int = 100000, min_length: int = 1) -> str:
        """Validate text length."""
        if not isinstance(text, str):
            raise ValidationError("Input must be a string")
        if len(text) < min_length:
            raise ValidationError(f"Input length {len(text)} is below minimum {min_length}")
        if len(text) > max_length:
            raise ValidationError(f"Input length {len(text)} exceeds maximum {max_length}")
        return text
    
    @staticmethod
    def validate_pattern(text: str, pattern_name: str) -> bool:
        """Validate text against a named pattern."""
        if pattern_name not in InputValidator.PATTERNS:
            raise ValidationError(f"Unknown pattern: {pattern_name}")
        return bool(re.match(InputValidator.PATTERNS[pattern_name], text))
    
    @staticmethod
    def check_safety(text: str) -> None:
        """Check for potentially unsafe content."""
        for pattern in InputValidator.UNSAFE_PATTERNS:
            if re.search(pattern, text):
                raise InputSafetyError(f"Input contains potentially unsafe content matching pattern: {pattern}")
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize input text."""
        # Remove null bytes
        text = text.replace('\0', '')
        # Remove control characters except newlines and tabs
        text = ''.join(char for char in text if char == '\n' or char == '\t' or (ord(char) >= 32 and ord(char) != 127))
        return text

def validate_llm_input(
    prompt: str,
    max_length: int = 100000,
    check_safety: bool = True,
    sanitize: bool = True
) -> str:
    """Validate and sanitize LLM input."""
    logger.debug(f"Validating LLM input (length: {len(prompt)})")
    
    if sanitize:
        prompt = InputValidator.sanitize_input(prompt)
    
    try:
        prompt = InputValidator.validate_length(prompt, max_length)
        if check_safety:
            InputValidator.check_safety(prompt)
        return prompt
    except (ValidationError, InputSafetyError) as e:
        logger.error(f"Input validation failed: {str(e)}")
        raise

def validate_embedding_input(
    text: str,
    max_length: int = 50000,
    sanitize: bool = True
) -> str:
    """Validate and sanitize embedding input."""
    logger.debug(f"Validating embedding input (length: {len(text)})")
    
    if sanitize:
        text = InputValidator.sanitize_input(text)
    
    try:
        return InputValidator.validate_length(text, max_length)
    except ValidationError as e:
        logger.error(f"Embedding input validation failed: {str(e)}")
        raise

def validate_vector_input(
    vectors: List[List[float]],
    dimension: Optional[int] = None
) -> None:
    """Validate vector input for vector store."""
    if not vectors:
        raise ValidationError("Empty vector list")
    
    if dimension and any(len(v) != dimension for v in vectors):
        raise ValidationError(f"All vectors must have dimension {dimension}")
    
    if any(not isinstance(x, (int, float)) for v in vectors for x in v):
        raise ValidationError("Vectors must contain only numbers")

def validate_search_query(
    query: str,
    max_length: int = 1000,
    check_safety: bool = True,
    sanitize: bool = True
) -> str:
    """Validate and sanitize search query."""
    logger.debug(f"Validating search query: {query}")
    
    if sanitize:
        query = InputValidator.sanitize_input(query)
    
    try:
        query = InputValidator.validate_length(query, max_length)
        if check_safety:
            InputValidator.check_safety(query)
        return query
    except (ValidationError, InputSafetyError) as e:
        logger.error(f"Search query validation failed: {str(e)}")
        raise 