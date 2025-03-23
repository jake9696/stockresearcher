import logging
from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta

from .call_llm import call_llm
from .web_search import search_web
from .validation import validate_llm_input
from .errors import ValidationError

logger = logging.getLogger(__name__)

def analyze_stock_sentiment(ticker: str, days_back: int = 7) -> Dict[str, Any]:
    """
    Analyze market sentiment for a given stock by searching for recent news.
    
    Args:
        ticker: Stock ticker symbol
        days_back: How many days of news to analyze
        
    Returns:
        Dictionary containing sentiment analysis results
    """
    # Normalize ticker
    ticker = ticker.strip().upper()
    logger.info(f"Analyzing sentiment for {ticker} over past {days_back} days")
    
    # Search for recent news
    news_articles = fetch_recent_news(ticker, days_back)
    
    # Extract sentiment from news
    sentiment_results = extract_sentiment(ticker, news_articles)
    
    # Generate overall analysis
    overall_analysis = generate_sentiment_summary(ticker, sentiment_results)
    
    return {
        "ticker": ticker,
        "time_period": f"Past {days_back} days",
        "sentiment_score": sentiment_results.get("overall_score", 0),
        "sentiment_label": sentiment_results.get("overall_sentiment", "neutral"),
        "key_topics": sentiment_results.get("key_topics", []),
        "summary": overall_analysis,
        "news_count": len(news_articles)
    }

def fetch_recent_news(ticker: str, days_back: int = 7) -> List[Dict[str, Any]]:
    """
    Fetch recent news about a stock.
    
    Args:
        ticker: Stock ticker symbol
        days_back: How many days to look back
        
    Returns:
        List of news article dictionaries
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Format dates for search query
    date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
    
    # Create search queries
    search_queries = [
        f"{ticker} stock news {date_range}",
        f"{ticker} financial news {date_range}",
        f"{ticker} investor news {date_range}",
        f"{ticker} earnings {date_range}"
    ]
    
    all_results = []
    
    # Run searches
    for query in search_queries:
        try:
            logger.info(f"Searching for: {query}")
            results = search_web(query, max_results=5)
            
            # Process and deduplicate results
            for result in results:
                # Check if we already have this URL
                if not any(r.get("url") == result.get("url") for r in all_results):
                    all_results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("snippet", ""),
                        "date": result.get("date", "")
                    })
                    
                    # If we have enough results, stop
                    if len(all_results) >= 10:
                        break
                        
        except Exception as e:
            logger.warning(f"Error searching for {query}: {str(e)}")
    
    logger.info(f"Found {len(all_results)} news articles for {ticker}")
    return all_results

def extract_sentiment(ticker: str, news_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract sentiment from news articles using an LLM.
    
    Args:
        ticker: Stock ticker symbol
        news_articles: List of news article dictionaries
        
    Returns:
        Dictionary with sentiment analysis results
    """
    if not news_articles:
        logger.warning(f"No news articles found for {ticker}")
        return {
            "overall_sentiment": "neutral",
            "overall_score": 0,
            "key_topics": [],
            "article_sentiments": []
        }
    
    # Format news for the prompt
    news_context = []
    for i, article in enumerate(news_articles[:10]):  # Limit to 10 articles
        news_context.append(f"""
Article {i+1}:
Title: {article.get('title', 'Unknown')}
Date: {article.get('date', 'Unknown')}
Snippet: {article.get('snippet', 'No snippet available')}
URL: {article.get('url', 'No URL')}
""")
    
    news_text = "\n".join(news_context)
    
    # Create prompt for sentiment analysis
    prompt = f"""
You are a financial sentiment analyst examining news about {ticker} stock.

Recent news articles:
{news_text}

Analyze the sentiment in these articles toward {ticker}. For each article, determine if the sentiment is positive, negative, or neutral.
Then provide an overall sentiment analysis.

Return your analysis as a JSON object with this structure:
{{
  "overall_sentiment": "positive/negative/neutral",
  "overall_score": <number between -1 and 1>,
  "key_topics": ["topic1", "topic2", "topic3"],
  "article_sentiments": [
    {{
      "article_num": 1,
      "sentiment": "positive/negative/neutral",
      "score": <number between -1 and 1>,
      "key_points": ["point1", "point2"]
    }}
    // ... for each article
  ]
}}
"""
    
    # Validate the prompt
    validate_llm_input(prompt, "finance")
    
    # Call the LLM
    try:
        response = call_llm(prompt, use_cache=True, task_type="finance")
        
        # Try to parse JSON response
        try:
            sentiment_data = json.loads(response)
            
            # Basic validation
            required_keys = ["overall_sentiment", "overall_score", "key_topics", "article_sentiments"]
            for key in required_keys:
                if key not in sentiment_data:
                    sentiment_data[key] = [] if key == "key_topics" or key == "article_sentiments" else "neutral" if key == "overall_sentiment" else 0
            
            # Validate overall_score is in range
            if not -1 <= sentiment_data["overall_score"] <= 1:
                sentiment_data["overall_score"] = 0
                
            return sentiment_data
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse sentiment JSON response for {ticker}")
            # Return a default structure
            return {
                "overall_sentiment": "neutral",
                "overall_score": 0,
                "key_topics": [],
                "article_sentiments": []
            }
            
    except Exception as e:
        logger.error(f"Error extracting sentiment for {ticker}: {str(e)}")
        return {
            "overall_sentiment": "neutral",
            "overall_score": 0,
            "key_topics": [],
            "article_sentiments": [],
            "error": str(e)
        }

def generate_sentiment_summary(ticker: str, sentiment_results: Dict[str, Any]) -> str:
    """
    Generate a summary of sentiment analysis.
    
    Args:
        ticker: Stock ticker symbol
        sentiment_results: Results from extract_sentiment
        
    Returns:
        String with sentiment summary
    """
    # Create prompt for generating summary
    prompt = f"""
You are a financial analyst providing a summary of sentiment for {ticker} stock.

Sentiment analysis results:
```json
{json.dumps(sentiment_results, indent=2)}
```

Based on this sentiment analysis, write a concise paragraph (3-5 sentences) that summarizes:
1. The overall market sentiment toward {ticker}
2. The key topics or themes mentioned in the news
3. Any significant positive or negative points from the articles
4. The potential impact on the stock price (if discernible)

Write this in a professional tone appropriate for investors. Be balanced and mention both positive and negative aspects if present.
"""
    
    # Validate the prompt
    validate_llm_input(prompt, "finance")
    
    # Call the LLM
    try:
        response = call_llm(prompt, use_cache=True, task_type="finance")
        return response.strip()
    except Exception as e:
        logger.error(f"Error generating sentiment summary for {ticker}: {str(e)}")
        return f"Unable to generate sentiment summary due to an error: {str(e)}"

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Test the sentiment analysis
    ticker = "AAPL"
    days = 3
    
    try:
        print(f"Analyzing sentiment for {ticker} over past {days} days...")
        sentiment = analyze_stock_sentiment(ticker, days)
        
        print(f"\nSentiment Analysis Results for {ticker}:")
        print(f"Sentiment: {sentiment['sentiment_label']} (Score: {sentiment['sentiment_score']})")
        print(f"Key Topics: {', '.join(sentiment['key_topics'])}")
        print(f"News Articles Analyzed: {sentiment['news_count']}")
        print(f"\nSummary:\n{sentiment['summary']}")
    except Exception as e:
        print(f"Error: {str(e)}") 