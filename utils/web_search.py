import requests
import os
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search the web using Brave Search API.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        
    Returns:
        List of dicts with keys: title, url, snippet
    """
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        raise ValueError("BRAVE_API_KEY environment variable not set")
        
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    
    params = {
        "q": query,
        "count": max_results
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("web", {}).get("results", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "snippet": item.get("description")
            })
            
        logger.info(f"Found {len(results)} results for query: {query}")
        return results
        
    except Exception as e:
        logger.error(f"Error searching web: {str(e)}")
        raise

if __name__ == "__main__":
    # Test the function
    results = search_web("Python programming")
    for r in results:
        print(f"Title: {r['title']}\nURL: {r['url']}\n") 