from pocketflow import Node, BatchNode
import logging
from typing import Dict, Any, List, Optional
import json
import re

from utils import (
    call_llm, get_logger, validate_llm_input, 
    fetch_stock_data, fetch_market_data,
    analyze_stock_financials, analyze_stock_sentiment,
    compare_financials
)

# Configure logging
logger = get_logger(__name__)

class GetUserQueryNode(Node):
    """Node to get the user's stock research query."""
    
    def exec(self, _):
        """Get user query directly from user input."""
        user_query = input("\nEnter a stock ticker or research query (e.g., 'AAPL' or 'Compare AAPL and MSFT'): ")
        return user_query.strip()
    
    def post(self, shared, prep_res, exec_res):
        """Store the user's query and determine the next action."""
        shared["user_query"] = exec_res
        
        # Parse the query to determine what the user is asking for
        if self._is_single_ticker(exec_res):
            # Single stock analysis
            ticker = self._extract_ticker(exec_res)
            shared["ticker"] = ticker
            logger.info(f"Single stock analysis requested for {ticker}")
            return "single_stock"
            
        elif self._is_comparison_query(exec_res):
            # Comparison between stocks
            tickers = self._extract_multiple_tickers(exec_res)
            shared["tickers"] = tickers
            logger.info(f"Comparison requested between {', '.join(tickers)}")
            return "compare_stocks"
            
        else:
            # Custom research query
            logger.info(f"Custom research query: {exec_res}")
            return "custom_query"
    
    def _is_single_ticker(self, query: str) -> bool:
        """Check if the query is just a single stock ticker."""
        # A single ticker is typically 1-5 uppercase letters
        return bool(re.match(r'^[A-Z]{1,5}$', query.strip().upper()))
    
    def _is_comparison_query(self, query: str) -> bool:
        """Check if the query is asking for a comparison between stocks."""
        query = query.upper()
        # Check for comparison keywords and multiple tickers
        comparison_keywords = ["COMPARE", "VS", "VERSUS", "AGAINST", "AND"]
        has_comparison_word = any(keyword in query.split() for keyword in comparison_keywords)
        
        # Check if multiple tickers are present
        tickers = self._extract_multiple_tickers(query)
        return has_comparison_word and len(tickers) >= 2
    
    def _extract_ticker(self, query: str) -> str:
        """Extract a single ticker from the query."""
        # First check if it's already just a ticker
        if self._is_single_ticker(query):
            return query.strip().upper()
        
        # Otherwise try to extract from the query
        # This is a simplified approach - in a real app, this would be more sophisticated
        matches = re.findall(r'\b[A-Z]{1,5}\b', query.upper())
        if matches:
            return matches[0]
        
        return "AAPL"  # Default to AAPL if no ticker found
    
    def _extract_multiple_tickers(self, query: str) -> List[str]:
        """Extract multiple tickers from the query."""
        # Find all word patterns that look like tickers (1-5 uppercase letters)
        matches = re.findall(r'\b[A-Z]{1,5}\b', query.upper())
        
        # Filter out common words that might match the pattern but aren't tickers
        common_words = ["A", "I", "AM", "AN", "AS", "AT", "BE", "BY", "FOR", "IN", "IS", "IT", "OF", "ON", "OR", "TO", "VS"]
        tickers = [match for match in matches if match not in common_words]
        
        # If no tickers found, return a default
        if not tickers:
            return ["AAPL", "MSFT"]
        
        return tickers


class FetchStockDataNode(Node):
    """Node to fetch stock data for a single ticker."""
    
    def prep(self, shared):
        """Get the ticker from shared store."""
        return shared["ticker"]
    
    def exec(self, ticker):
        """Fetch the stock data for the ticker."""
        logger.info(f"Fetching data for {ticker}")
        stock_data = fetch_stock_data(ticker)
        
        # Also fetch market data for the stock's sector
        sector = stock_data.get("company_info", {}).get("sector", "Technology")
        market_data = fetch_market_data(sector)
        
        return stock_data, market_data
    
    def post(self, shared, prep_res, exec_res):
        """Store the stock data and market data."""
        stock_data, market_data = exec_res
        shared["stock_data"] = stock_data
        shared["market_data"] = market_data
        return "default"


class AnalyzeStockNode(Node):
    """Node to analyze a single stock."""
    
    def prep(self, shared):
        """Get the stock data and market data from shared store."""
        return shared["stock_data"], shared["market_data"]
    
    def exec(self, data):
        """Analyze the stock data."""
        stock_data, market_data = data
        ticker = stock_data["ticker"]
        
        logger.info(f"Analyzing {ticker}")
        
        # Financial analysis
        financial_analysis = analyze_stock_financials(stock_data)
        
        # Sentiment analysis
        sentiment_analysis = analyze_stock_sentiment(ticker)
        
        # Return all analyses
        return {
            "ticker": ticker,
            "financial_analysis": financial_analysis,
            "sentiment_analysis": sentiment_analysis,
            "market_data": market_data
        }
    
    def post(self, shared, prep_res, exec_res):
        """Store the analysis results."""
        shared["analysis_results"] = exec_res
        return "default"


class GenerateStockReportNode(Node):
    """Node to generate a report for a single stock."""
    
    def prep(self, shared):
        """Get the analysis results from shared store."""
        return shared["analysis_results"]
    
    def exec(self, analysis_results):
        """Generate a comprehensive report about the stock."""
        ticker = analysis_results["ticker"]
        financial = analysis_results["financial_analysis"]
        sentiment = analysis_results["sentiment_analysis"]
        market = analysis_results["market_data"]
        
        # Create prompt context
        context = {
            "ticker": ticker,
            "company_name": analysis_results.get("stock_data", {}).get("company_info", {}).get("name", f"{ticker} Inc."),
            "financial_ratios": financial.get("ratios", {}),
            "financial_trends": financial.get("trends", {}),
            "financial_insights": financial.get("insights", []),
            "sentiment_score": sentiment.get("sentiment_score", 0),
            "sentiment_label": sentiment.get("sentiment_label", "neutral"),
            "key_topics": sentiment.get("key_topics", []),
            "sentiment_summary": sentiment.get("summary", ""),
            "sector": market.get("sector", "Unknown"),
            "competitors": [comp.get("ticker") for comp in market.get("competitors", [])][:5]
        }
        
        # Convert to JSON string for the prompt
        context_str = json.dumps(context, indent=2)
        
        # Create prompt for generating the report
        prompt = f"""
You are a professional stock analyst preparing a comprehensive report for {ticker}.

Analysis data:
```json
{context_str}
```

Based on this analysis data, write a detailed stock analysis report for {ticker}. Include:

1. An executive summary (1-2 paragraphs)
2. Financial Health Analysis
   - Key financial ratios and what they indicate
   - Financial trends and their implications
   - Strengths and weaknesses in the financials
3. Market Sentiment Analysis
   - Current sentiment and key topics/themes
   - Implications of the sentiment on potential stock movement
4. Competitive Position
   - How the company compares to its sector
   - Key competitors and their impact
5. Outlook and Recommendation
   - Future prospects based on all the above
   - A clear investment recommendation (Buy/Hold/Sell)

Format this as a professional report with clear sections and bullet points where appropriate.
"""
        
        # Validate the prompt
        validate_llm_input(prompt, "finance")
        
        # Generate the report
        try:
            report = call_llm(prompt, use_cache=True, task_type="finance")
            return report
        except Exception as e:
            logger.error(f"Error generating report for {ticker}: {str(e)}")
            return f"Error generating report: {str(e)}"
    
    def post(self, shared, prep_res, exec_res):
        """Store the generated report."""
        shared["report"] = exec_res
        return "default"


class BatchFetchStockDataNode(BatchNode):
    """Batch node to fetch data for multiple stocks."""
    
    def prep(self, shared):
        """Get the list of tickers from shared store."""
        return shared["tickers"]
    
    def exec(self, ticker):
        """Fetch data for a single ticker in the batch."""
        logger.info(f"Batch fetching data for {ticker}")
        stock_data = fetch_stock_data(ticker)
        return stock_data
    
    def post(self, shared, prep_res, exec_res_list):
        """Store all the fetched stock data."""
        # Create a dictionary of ticker -> data
        stocks_data = {data["ticker"]: data for data in exec_res_list}
        shared["stocks_data"] = stocks_data
        
        # Also fetch market data for the first stock's sector
        if exec_res_list:
            sector = exec_res_list[0].get("company_info", {}).get("sector", "Technology")
            shared["market_data"] = fetch_market_data(sector)
        
        return "default"


class CompareStocksNode(Node):
    """Node to compare multiple stocks."""
    
    def prep(self, shared):
        """Get the stocks data from shared store."""
        return shared["stocks_data"]
    
    def exec(self, stocks_data):
        """Compare the stocks."""
        logger.info(f"Comparing {len(stocks_data)} stocks")
        
        # Convert to list for the comparison function
        stocks_list = list(stocks_data.values())
        
        # Perform comparison
        comparison_results = compare_financials(stocks_list)
        
        return comparison_results
    
    def post(self, shared, prep_res, exec_res):
        """Store the comparison results."""
        shared["comparison_results"] = exec_res
        return "default"


class GenerateComparisonReportNode(Node):
    """Node to generate a comparison report for multiple stocks."""
    
    def prep(self, shared):
        """Get the comparison results and stocks data from shared store."""
        return shared["comparison_results"], shared["stocks_data"], shared["market_data"]
    
    def exec(self, data):
        """Generate a comparison report."""
        comparison_results, stocks_data, market_data = data
        
        tickers = comparison_results["tickers"]
        ratio_comparison = comparison_results["ratio_comparison"]
        insights = comparison_results["insights"]
        
        # Create context for the prompt
        stocks_info = []
        for ticker in tickers:
            stock_data = stocks_data.get(ticker, {})
            stocks_info.append({
                "ticker": ticker,
                "name": stock_data.get("company_info", {}).get("name", f"{ticker} Inc."),
                "sector": stock_data.get("company_info", {}).get("sector", "Technology"),
                "industry": stock_data.get("company_info", {}).get("industry", "Software")
            })
        
        context = {
            "tickers": tickers,
            "stocks_info": stocks_info,
            "ratio_comparison": ratio_comparison,
            "insights": insights,
            "sector": market_data.get("sector", "Technology"),
            "segment_etf": market_data.get("segment_etf", "SPY")
        }
        
        # Convert to JSON string for the prompt
        context_str = json.dumps(context, indent=2)
        
        # Create prompt for generating the report
        ticker_list = ", ".join(tickers)
        prompt = f"""
You are a professional stock analyst preparing a comparative analysis report for {ticker_list}.

Comparison data:
```json
{context_str}
```

Based on this data, write a detailed comparison report for these stocks. Include:

1. An executive summary of the comparison (1-2 paragraphs)
2. Company Profiles
   - Brief description of each company
   - Their primary business and market position
3. Financial Comparison
   - Side-by-side analysis of key financial ratios
   - Relative strengths and weaknesses
4. Investment Outlook
   - Which company(s) appear to be better investments and why
   - Risk factors for each
5. Recommendation
   - Ranked order of investment preference
   - Specific recommendation for each stock (Buy/Hold/Sell)

Format this as a professional report with clear sections and tables/bullet points where appropriate.
"""
        
        # Validate the prompt
        validate_llm_input(prompt, "finance")
        
        # Generate the report
        try:
            report = call_llm(prompt, use_cache=True, task_type="finance")
            return report
        except Exception as e:
            logger.error(f"Error generating comparison report: {str(e)}")
            return f"Error generating report: {str(e)}"
    
    def post(self, shared, prep_res, exec_res):
        """Store the generated report."""
        shared["report"] = exec_res
        return "default"


class CustomResearchNode(Node):
    """Node to handle custom research queries."""
    
    def prep(self, shared):
        """Get the user query from shared store."""
        return shared["user_query"]
    
    def exec(self, query):
        """Execute the custom research query."""
        logger.info(f"Executing custom research: {query}")
        
        # Extract potential tickers from the query
        tickers = re.findall(r'\b[A-Z]{1,5}\b', query.upper())
        common_words = ["A", "I", "AM", "AN", "AS", "AT", "BE", "BY", "FOR", "IN", "IS", "IT", "OF", "ON", "OR", "TO", "VS"]
        tickers = [ticker for ticker in tickers if ticker not in common_words]
        
        # Fetch basic data for mentioned tickers
        ticker_data = {}
        if tickers:
            logger.info(f"Found potential tickers in query: {', '.join(tickers)}")
            for ticker in tickers[:3]:  # Limit to first 3 tickers
                try:
                    ticker_data[ticker] = fetch_stock_data(ticker)
                except Exception as e:
                    logger.warning(f"Error fetching data for {ticker}: {str(e)}")
        
        # Generate a research brief based on the query
        prompt = f"""
You are a professional stock analyst and financial researcher. A user has asked the following question:

"{query}"

Based on this question, provide a detailed and informative response. If specific stocks were mentioned, include relevant information about them.

Here is some basic data for stocks mentioned in the query:
```json
{json.dumps(ticker_data, indent=2)}
```

Your response should:
1. Directly address the user's question with factual information
2. Provide context about any companies or financial concepts mentioned
3. Include specific data points when available
4. Offer a balanced perspective on investment considerations
5. Conclude with actionable insights or recommendations if appropriate

Format your response as a professional research brief with clear sections.
"""
        
        # Validate the prompt
        validate_llm_input(prompt, "finance")
        
        # Generate the response
        try:
            research = call_llm(prompt, use_cache=True, task_type="finance")
            return research
        except Exception as e:
            logger.error(f"Error generating custom research: {str(e)}")
            return f"Error generating research: {str(e)}"
    
    def post(self, shared, prep_res, exec_res):
        """Store the generated research."""
        shared["report"] = exec_res
        return "default"


class DisplayReportNode(Node):
    """Node to display the final report to the user."""
    
    def prep(self, shared):
        """Get the report from shared store."""
        return shared["report"]
    
    def exec(self, report):
        """Display the report."""
        # No further processing needed, just return
        return report
    
    def post(self, shared, prep_res, exec_res):
        """Display the report and ask if the user wants to continue."""
        print("\n" + "="*80)
        print("STOCK ANALYSIS REPORT")
        print("="*80 + "\n")
        print(exec_res)
        print("\n" + "="*80)
        
        # Ask if the user wants to continue
        continue_response = input("\nWould you like to research another stock? (y/n): ")
        if continue_response.lower().strip() in ('y', 'yes'):
            return "continue"
        else:
            return "exit"