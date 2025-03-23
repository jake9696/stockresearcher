import os
import requests
import logging
import json
import time
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple, List

from .errors import APIError, RateLimitError
from .rate_limiter import wait_for_rate_limit
from .validation import validate_llm_input

logger = logging.getLogger(__name__)

def fetch_stock_data(ticker: str, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Fetch stock data for a given ticker, with caching.
    
    Args:
        ticker: Stock ticker symbol
        force_refresh: Whether to force a refresh of the data
        
    Returns:
        Dictionary containing stock data
    """
    # Normalize ticker
    ticker = ticker.strip().upper()
    
    # Check for cached data if not forcing refresh
    if not force_refresh:
        cached_data = _get_cached_data(ticker)
        if cached_data:
            logger.info(f"Using cached data for {ticker}")
            return cached_data
    
    logger.info(f"Fetching fresh data for {ticker}")
    
    # Attempt to fetch from primary source
    try:
        # Wait for rate limit availability
        wait_for_rate_limit("stock_api", max_retries=3)
        data = _fetch_from_yfinance(ticker)
        _cache_data(ticker, data)
        return data
    except Exception as e:
        logger.warning(f"Primary source failed for {ticker}: {str(e)}")
        
        # Try fallback source
        try:
            wait_for_rate_limit("fallback_api", max_retries=3)
            data = _fetch_from_fallback(ticker)
            _cache_data(ticker, data)
            return data
        except Exception as e2:
            logger.error(f"All sources failed for {ticker}: {str(e2)}")
            raise APIError(f"Failed to fetch data for {ticker}: {str(e2)}")

def _get_cached_data(ticker: str) -> Optional[Dict[str, Any]]:
    """Get cached data if available and not expired."""
    cache_file = f"data/cache/{ticker.lower()}_stock_data.json"
    
    # Ensure cache directory exists
    os.makedirs("data/cache", exist_ok=True)
    
    if not os.path.exists(cache_file):
        return None
        
    # Check if cache is expired (older than 1 day)
    file_mod_time = os.path.getmtime(cache_file)
    if (time.time() - file_mod_time) > 86400:  # 24 hours
        logger.info(f"Cache expired for {ticker}")
        return None
        
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.warning(f"Error reading cache for {ticker}: {str(e)}")
        return None

def _cache_data(ticker: str, data: Dict[str, Any]) -> None:
    """Cache the stock data to file."""
    cache_file = f"data/cache/{ticker.lower()}_stock_data.json"
    
    # Ensure cache directory exists
    os.makedirs("data/cache", exist_ok=True)
    
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        logger.info(f"Successfully cached data for {ticker}")
    except Exception as e:
        logger.warning(f"Failed to cache data for {ticker}: {str(e)}")

def _fetch_from_yfinance(ticker: str) -> Dict[str, Any]:
    """
    Fetch stock data from Yahoo Finance.
    This is a placeholder - in a real app, use yfinance library or its API.
    """
    # This is a simplified mock implementation
    # In a real app, you would use the yfinance library
    api_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    
    try:
        response = requests.get(api_url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        response.raise_for_status()
        
        # Process the data
        # This is a simplified version - actual implementation would be more complex
        result = {
            "ticker": ticker,
            "last_updated": datetime.now().isoformat(),
            "price_data": {
                "daily": [],  # Would contain actual price data
                "weekly": [], 
                "monthly": []
            },
            "financials": {
                "income_statement": {},
                "balance_sheet": {},
                "cash_flow": {}
            },
            "company_info": {
                "name": f"{ticker} Inc.",  # Placeholder
                "sector": "Technology",    # Placeholder
                "industry": "Software",    # Placeholder
            }
        }
        
        # Add mock data for demo purposes
        # In a real app, this would be parsed from the API response
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching from Yahoo Finance: {str(e)}")
        raise APIError(f"Yahoo Finance API error: {str(e)}")

def _fetch_from_fallback(ticker: str) -> Dict[str, Any]:
    """
    Fallback data source when primary fails.
    This is a placeholder - in a real app, use another API.
    """
    # This is a mock implementation
    # In a real app, you would integrate with another financial data API
    
    # For demo purposes, return similar structure as the primary source
    return {
        "ticker": ticker,
        "last_updated": datetime.now().isoformat(),
        "price_data": {
            "daily": [],  # Would contain actual price data 
            "weekly": [],
            "monthly": []
        },
        "financials": {
            "income_statement": {},
            "balance_sheet": {},
            "cash_flow": {}
        },
        "company_info": {
            "name": f"{ticker} Corporation",  # Placeholder
            "sector": "Technology",           # Placeholder
            "industry": "Software",           # Placeholder
        }
    }

def fetch_market_data(sector: str) -> Dict[str, Any]:
    """
    Fetch market data for a given sector.
    
    Args:
        sector: The sector to fetch data for
        
    Returns:
        Dictionary containing market data and competitors
    """
    # This is a mock implementation
    # In a real app, you would fetch actual market and competitor data
    
    # Mock data for demonstration purposes
    sector_etfs = {
        "Technology": "XLK",
        "Healthcare": "XLV",
        "Financials": "XLF",
        "Consumer Discretionary": "XLY",
        "Energy": "XLE"
    }
    
    sector_companies = {
        "Technology": ["AAPL", "MSFT", "GOOGL", "META", "AMZN"],
        "Healthcare": ["JNJ", "PFE", "MRK", "UNH", "ABBV"],
        "Financials": ["JPM", "BAC", "WFC", "C", "GS"],
        "Consumer Discretionary": ["AMZN", "HD", "MCD", "NKE", "SBUX"],
        "Energy": ["XOM", "CVX", "COP", "EOG", "SLB"]
    }
    
    # Get ETF for the sector
    etf = sector_etfs.get(sector, "SPY")  # Default to SPY if sector not found
    
    # Get competitors for the sector
    competitors = [
        {"ticker": comp, "name": f"{comp} Inc.", "market_cap": 1000000000}
        for comp in sector_companies.get(sector, ["AAPL", "MSFT", "GOOGL"])
    ]
    
    return {
        "sector": sector,
        "segment_etf": etf,
        "segment_data": {},  # Would contain actual sector data
        "spy_data": {},      # Would contain S&P 500 data
        "competitors": competitors
    }

if __name__ == "__main__":
    # Configure logging for standalone testing
    logging.basicConfig(level=logging.INFO)
    
    # Test the function
    ticker = "AAPL"
    print(f"Testing fetch_stock_data for {ticker}:")
    try:
        data = fetch_stock_data(ticker)
        print(f"Successfully fetched data for {ticker}")
        print(f"Company name: {data['company_info']['name']}")
        print(f"Sector: {data['company_info']['sector']}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test market data function
    print("\nTesting fetch_market_data for Technology sector:")
    try:
        market_data = fetch_market_data("Technology")
        print(f"Sector ETF: {market_data['segment_etf']}")
        print(f"Competitors: {[comp['ticker'] for comp in market_data['competitors']]}")
    except Exception as e:
        print(f"Error: {str(e)}") 