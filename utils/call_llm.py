import os
import requests
from functools import lru_cache
import logging
from typing import Literal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LLMType = Literal["thinking", "basic", "code", "creative", "math"]

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
@lru_cache(maxsize=1000)
def cached_call(prompt: str, llm_type: LLMType):
    """Cached version of the LLM call."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    
    # Select model based on task type
    if llm_type in ["thinking", "code", "creative", "math"]:
        model = "anthropic/claude-3-sonnet:thinking"
    else:
        model = "google/gemini-2.0-flash-exp:free"
        
    logger.info(f"Prompt to {model} for {llm_type} task: {prompt[:100]}...")
    
    # Customize the prompt based on task type
    if llm_type == "code":
        prompt = f"""You are an expert programmer. Please analyze or generate code with detailed explanations.

Task: {prompt}"""
    elif llm_type == "creative":
        prompt = f"""You are a creative writer with expertise in engaging and imaginative content creation.

Task: {prompt}"""
    elif llm_type == "math":
        prompt = f"""You are a mathematical expert. Please solve or explain mathematical concepts with clear step-by-step reasoning.

Task: {prompt}"""
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/your-repo",  # Replace with your repo
                "X-Title": "Stock Researcher"  # Replace with your app name
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                # Add specific parameters for Claude
                "temperature": 0.7 if llm_type == "creative" else 0.2,  # Higher temp for creative tasks
                "max_tokens": 500000,  # Default to maximum possible context
                "stop": None
            }
        )
        response.raise_for_status()
        result = response.json()
        response_text = result["choices"][0]["message"]["content"]
        logger.info(f"Response: {response_text[:100]}...")
        return response_text
    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}")
        raise

def call_llm(prompt: str, llm_type: LLMType = "basic", use_cache: bool = True):
    """
    Main LLM call function with optional caching.
    
    Args:
        prompt: The prompt to send to the LLM
        llm_type: Type of task - one of:
            - "thinking": Complex reasoning tasks
            - "basic": Simple, straightforward tasks
            - "code": Code generation and analysis
            - "creative": Creative writing tasks
            - "math": Mathematical computations and explanations
        use_cache: Whether to use caching
    """
    if use_cache:
        return cached_call(prompt, llm_type)
    return cached_call.__wrapped__(prompt, llm_type)

if __name__ == "__main__":
    # Test different types of calls
    tests = {
        "basic": "What is 2+2?",
        "thinking": "Explain the implications of quantum entanglement on information theory",
        "code": "Write a Python function to find the nth Fibonacci number using dynamic programming",
        "creative": "Write a short story about a robot discovering emotions",
        "math": "Solve the differential equation dy/dx = 2x + y with initial condition y(0) = 1"
    }
    
    for task_type, prompt in tests.items():
        print(f"\n=== Testing {task_type.upper()} task ===")
        print(f"Prompt: {prompt}")
        print(f"Response: {call_llm(prompt, llm_type=task_type)}\n")
