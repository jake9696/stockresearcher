import logging
import os
from flow import create_stock_analysis_flow

def configure_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # File handler for detailed logs
            logging.FileHandler("logs/stock_analysis.log"),
            # Console handler for important messages
            logging.StreamHandler()
        ]
    )
    
    # Set more restrictive log level for some noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    return logging.getLogger("main")

def main():
    """Main application entry point."""
    # Configure logging
    logger = configure_logging()
    logger.info("Starting Stock Analysis Application")
    
    # Initialize shared data store
    shared = {}
    
    # Create and run the stock analysis flow
    try:
        flow = create_stock_analysis_flow()
        flow.run(shared)
        logger.info("Flow execution completed successfully")
    except Exception as e:
        logger.error(f"Error during flow execution: {str(e)}")
        print(f"\nAn error occurred: {str(e)}")
        print("Please check the logs for more details.")
    
    logger.info("Application terminated")

if __name__ == "__main__":
    main()