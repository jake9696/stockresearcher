from pocketflow import Flow
from nodes import (
    GetUserQueryNode, 
    FetchStockDataNode, 
    AnalyzeStockNode, 
    GenerateStockReportNode,
    BatchFetchStockDataNode,
    CompareStocksNode,
    GenerateComparisonReportNode,
    CustomResearchNode,
    DisplayReportNode
)

def create_stock_analysis_flow():
    """
    Create and return the main stock analysis flow.
    
    This flow implements a workflow that:
    1. Gets a user query (ticker, comparison, or research question)
    2. Routes to the appropriate sub-flow based on query type
    3. Displays the resulting report
    4. Optionally loops back for more analysis
    """
    # Create all nodes
    get_query = GetUserQueryNode()
    display_report = DisplayReportNode()
    
    # Create the sub-flows
    single_stock_flow = create_single_stock_flow()
    comparison_flow = create_comparison_flow()
    custom_research_flow = create_custom_research_flow()
    
    # Connect the flows
    get_query - "single_stock" >> single_stock_flow
    get_query - "compare_stocks" >> comparison_flow
    get_query - "custom_query" >> custom_research_flow
    
    # All flows lead to display_report
    single_stock_flow >> display_report
    comparison_flow >> display_report
    custom_research_flow >> display_report
    
    # Loop back or exit
    display_report - "continue" >> get_query
    
    # Create the main flow
    return Flow(start=get_query)

def create_single_stock_flow():
    """Create a flow for analyzing a single stock."""
    # Create the nodes
    fetch_data = FetchStockDataNode()
    analyze_stock = AnalyzeStockNode()
    generate_report = GenerateStockReportNode()
    
    # Connect the nodes in sequence
    fetch_data >> analyze_stock >> generate_report
    
    # Create and return the flow
    return Flow(start=fetch_data)

def create_comparison_flow():
    """Create a flow for comparing multiple stocks."""
    # Create the nodes
    batch_fetch = BatchFetchStockDataNode()
    compare_stocks = CompareStocksNode()
    generate_report = GenerateComparisonReportNode()
    
    # Connect the nodes in sequence
    batch_fetch >> compare_stocks >> generate_report
    
    # Create and return the flow
    return Flow(start=batch_fetch)

def create_custom_research_flow():
    """Create a flow for custom research queries."""
    # Create the node
    custom_research = CustomResearchNode()
    
    # Create and return the flow (single node)
    return Flow(start=custom_research)

# This function is for backwards compatibility with the existing main.py
def create_qa_flow():
    """Create a question-answering flow (legacy function)."""
    return create_stock_analysis_flow()