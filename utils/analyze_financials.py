import logging
from typing import Dict, Any, List, Tuple
import json

from .call_llm import call_llm
from .errors import ValidationError
from .validation import validate_llm_input

logger = logging.getLogger(__name__)

def analyze_stock_financials(stock_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze financial data for a given stock.
    
    Args:
        stock_data: Stock data dictionary from fetch_stock_data
        
    Returns:
        Dictionary containing financial analysis results
    """
    ticker = stock_data.get("ticker")
    if not ticker:
        raise ValidationError("Stock data missing ticker symbol")
    
    logger.info(f"Analyzing financials for {ticker}")
    
    # Extract financial statements from the stock data
    financials = stock_data.get("financials", {})
    
    # Calculate financial ratios
    ratios = calculate_financial_ratios(financials)
    
    # Perform trend analysis
    trends = identify_financial_trends(financials)
    
    # Generate financial insights using LLM
    insights = generate_financial_insights(ticker, financials, ratios, trends)
    
    return {
        "ticker": ticker,
        "ratios": ratios,
        "trends": trends,
        "insights": insights
    }

def calculate_financial_ratios(financials: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate key financial ratios from financial statements.
    
    This is a placeholder implementation - in a real app, 
    this would perform actual calculations based on the data.
    """
    # Mock implementation for demo purposes
    # In a real app, these would be calculated from actual financial data
    return {
        "pe_ratio": 25.5,
        "price_to_sales": 7.2,
        "price_to_book": 12.3,
        "debt_to_equity": 0.45,
        "return_on_equity": 0.22,
        "gross_margin": 0.42,
        "operating_margin": 0.28,
        "net_margin": 0.21,
        "current_ratio": 1.8,
        "quick_ratio": 1.5
    }

def identify_financial_trends(financials: Dict[str, Any]) -> Dict[str, str]:
    """
    Identify trends in financial data.
    
    This is a placeholder implementation - in a real app,
    this would analyze actual data over time.
    """
    # Mock implementation for demo purposes
    # In a real app, these would be based on actual trend analysis
    return {
        "revenue_trend": "increasing",
        "profit_trend": "stable",
        "margin_trend": "decreasing",
        "debt_trend": "stable",
        "cash_flow_trend": "increasing",
        "r_and_d_trend": "increasing"
    }

def generate_financial_insights(
    ticker: str, 
    financials: Dict[str, Any], 
    ratios: Dict[str, float], 
    trends: Dict[str, str]
) -> List[str]:
    """
    Generate insights about the company's financials using an LLM.
    """
    # Create a context for the LLM with the financial data
    context = {
        "ticker": ticker,
        "financials": financials,
        "ratios": ratios,
        "trends": trends
    }
    
    # Convert to JSON string for the prompt
    context_str = json.dumps(context, indent=2)
    
    # Create a prompt for the LLM
    prompt = f"""
You are a financial analyst examining {ticker}'s financial data.

Financial data:
```json
{context_str}
```

Based on this financial data, provide 3-5 key insights about the company's financial health, performance, and outlook.
Each insight should be concise and data-driven. Focus on the most important aspects that an investor should know.

Format your response as a JSON array of strings, with each string being a specific insight.
"""
    
    # Validate the prompt
    validate_llm_input(prompt, "finance")
    
    # Call the LLM
    try:
        response = call_llm(prompt, use_cache=True, task_type="finance")
        
        # Parse the JSON response
        insights = json.loads(response)
        
        # Ensure we have a list of strings
        if not isinstance(insights, list):
            logger.warning(f"Expected list response for {ticker} insights, got {type(insights)}")
            insights = ["Failed to generate proper insights format"]
        
        return insights
        
    except Exception as e:
        logger.error(f"Error generating financial insights for {ticker}: {str(e)}")
        return [f"Error generating insights: {str(e)}"]

def compare_financials(stocks_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare financial data across multiple stocks.
    
    Args:
        stocks_data: List of stock data dictionaries
        
    Returns:
        Dictionary containing comparative analysis
    """
    if not stocks_data or len(stocks_data) < 2:
        raise ValidationError("Need at least 2 stocks for comparison")
    
    tickers = [data.get("ticker", "Unknown") for data in stocks_data]
    logger.info(f"Comparing financials for {', '.join(tickers)}")
    
    # Extract ratios for each stock
    all_ratios = {}
    for stock in stocks_data:
        ticker = stock.get("ticker", "Unknown")
        financials = stock.get("financials", {})
        all_ratios[ticker] = calculate_financial_ratios(financials)
    
    # Generate comparison using LLM
    comparison_insights = generate_comparison_insights(tickers, all_ratios)
    
    return {
        "tickers": tickers,
        "ratio_comparison": all_ratios,
        "insights": comparison_insights
    }

def generate_comparison_insights(tickers: List[str], all_ratios: Dict[str, Dict[str, float]]) -> List[str]:
    """
    Generate insights comparing financial ratios across stocks.
    """
    # Convert to JSON string for the prompt
    context_str = json.dumps(all_ratios, indent=2)
    
    # Create a prompt for the LLM
    ticker_list = ", ".join(tickers)
    prompt = f"""
You are a financial analyst comparing the financial ratios of {ticker_list}.

Financial ratios:
```json
{context_str}
```

Based on these financial ratios, provide 3-5 key comparative insights between these companies.
Focus on strengths, weaknesses, and notable differences. Be specific and data-driven.

Format your response as a JSON array of strings, with each string being a specific comparative insight.
"""
    
    # Validate the prompt
    validate_llm_input(prompt, "finance")
    
    # Call the LLM
    try:
        response = call_llm(prompt, use_cache=True, task_type="finance")
        
        # Parse the JSON response
        insights = json.loads(response)
        
        # Ensure we have a list of strings
        if not isinstance(insights, list):
            logger.warning(f"Expected list response for comparison insights, got {type(insights)}")
            insights = ["Failed to generate proper insights format"]
        
        return insights
        
    except Exception as e:
        logger.error(f"Error generating comparison insights: {str(e)}")
        return [f"Error generating comparison insights: {str(e)}"]

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Mock stock data for testing
    mock_stock = {
        "ticker": "AAPL",
        "financials": {
            "income_statement": {},
            "balance_sheet": {},
            "cash_flow": {}
        }
    }
    
    # Test financial analysis
    try:
        analysis = analyze_stock_financials(mock_stock)
        print("Financial Analysis Results:")
        print(f"Ticker: {analysis['ticker']}")
        print(f"Ratios: {analysis['ratios']}")
        print(f"Trends: {analysis['trends']}")
        print(f"Insights: {analysis['insights']}")
    except Exception as e:
        print(f"Error: {str(e)}") 