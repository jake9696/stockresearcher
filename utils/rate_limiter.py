import time
from collections import deque
from dataclasses import dataclass
from typing import Dict, Deque
import logging
import threading

logger = logging.getLogger(__name__)

@dataclass
class RateLimit:
    rpm: int  # Requests per minute
    tpm: int = None  # Tokens per minute (optional)
    rpd: int = None  # Requests per day (optional)

class RateLimiter:
    def __init__(self, limits: Dict[str, RateLimit]):
        """
        Initialize rate limiter with limits for different services.
        
        Args:
            limits: Dict mapping service names to their RateLimit
        """
        self.limits = limits
        self.requests: Dict[str, Deque] = {}
        self.tokens: Dict[str, Deque] = {}
        self.daily_requests: Dict[str, Deque] = {}
        self.lock = threading.Lock()
        
        # Initialize tracking for each service
        for service in limits:
            self.requests[service] = deque()
            if limits[service].tpm:
                self.tokens[service] = deque()
            if limits[service].rpd:
                self.daily_requests[service] = deque()
    
    def _clean_old_entries(self, queue: Deque, window: int):
        """Remove entries older than the window (in seconds)."""
        now = time.time()
        while queue and now - queue[0] > window:
            queue.popleft()
    
    def can_make_request(self, service: str, token_count: int = 0) -> bool:
        """
        Check if a request can be made based on rate limits.
        
        Args:
            service: Service identifier (e.g., "gemini_embedding", "openrouter")
            token_count: Number of tokens in the request (if applicable)
        """
        with self.lock:
            now = time.time()
            limit = self.limits[service]
            
            # Clean old entries
            self._clean_old_entries(self.requests[service], 60)  # 1 minute window
            if service in self.tokens:
                self._clean_old_entries(self.tokens[service], 60)
            if service in self.daily_requests:
                self._clean_old_entries(self.daily_requests[service], 86400)  # 24 hour window
            
            # Check RPM
            if len(self.requests[service]) >= limit.rpm:
                logger.warning(f"{service} RPM limit reached ({limit.rpm})")
                return False
                
            # Check TPM
            if limit.tpm and token_count:
                current_tokens = sum(1 for _ in self.tokens[service])
                if current_tokens + token_count > limit.tpm:
                    logger.warning(f"{service} TPM limit reached ({limit.tpm})")
                    return False
                    
            # Check RPD
            if limit.rpd and len(self.daily_requests[service]) >= limit.rpd:
                logger.warning(f"{service} RPD limit reached ({limit.rpd})")
                return False
            
            return True
    
    def record_request(self, service: str, token_count: int = 0):
        """Record that a request was made."""
        with self.lock:
            now = time.time()
            self.requests[service].append(now)
            if service in self.tokens and token_count:
                for _ in range(token_count):
                    self.tokens[service].append(now)
            if service in self.daily_requests:
                self.daily_requests[service].append(now)

# Create a global rate limiter instance with our limits
RATE_LIMITS = {
    "gemini_embedding": RateLimit(rpm=5, rpd=100),  # Gemini embedding limits
    "gemini_basic": RateLimit(rpm=15, tpm=1_000_000, rpd=1500),  # Gemini Flash limits
    "openrouter": RateLimit(rpm=120)  # OpenRouter limits
}

rate_limiter = RateLimiter(RATE_LIMITS)

def wait_for_rate_limit(service: str, token_count: int = 0, max_retries: int = 5, retry_delay: float = 1.0) -> bool:
    """
    Wait until a request can be made within rate limits.
    
    Args:
        service: Service identifier
        token_count: Number of tokens in the request (if applicable)
        max_retries: Maximum number of times to retry
        retry_delay: Delay between retries in seconds
        
    Returns:
        bool: True if request can proceed, False if max retries exceeded
    """
    for attempt in range(max_retries):
        if rate_limiter.can_make_request(service, token_count):
            return True
        if attempt < max_retries - 1:
            delay = retry_delay * (2 ** attempt)  # Exponential backoff
            logger.info(f"Rate limit reached for {service}, waiting {delay:.1f}s...")
            time.sleep(delay)
    return False 