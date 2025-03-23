# Stock Analysis Application

A comprehensive tool for analyzing stocks from multiple perspectives, built with PocketFlow.

## Overview

This application analyzes stocks using:
- Financial data analysis
- Technical indicators
- Market sentiment and news analysis
- Competitor comparison

## Features

- **Single Stock Analysis**: Get a detailed report on any publicly traded stock
- **Stock Comparison**: Compare multiple stocks side by side
- **Custom Research**: Ask specific questions about stocks or markets
- **Interactive Reports**: Generate professional reports with insights and recommendations

## Getting Started

### Prerequisites

- Python 3.8 or later
- Required Python packages (install via `pip install -r requirements.txt`)
- API keys for external services:
  - Set as environment variables or in a `.env` file

### Installation

1. Clone the repository
```bash
git clone https://github.com/jake9696/stockresearcher.git
cd stockresearcher
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
# Create a .env file with your API keys
touch .env
# Edit the file to add your API keys
```

### Usage

Run the main application:
```bash
python main.py
```

You can interact with the application by:
1. Entering a stock ticker (e.g., "AAPL") for single stock analysis
2. Entering a comparison query (e.g., "Compare AAPL and MSFT") to compare stocks
3. Asking a custom research question (e.g., "What are the best tech stocks for long-term investment?")

The application will generate a comprehensive report based on your query.

## Architecture

This application is built using the PocketFlow framework, which provides a graph-based approach to workflow orchestration.

### Key Components

- **Nodes**: Individual processing units that handle specific tasks
- **Flows**: Orchestrate nodes into complete workflows
- **Utilities**: Handle external API calls and data processing

### Flow Structure

```
User Query → Query Parsing → Data Collection → Analysis → Report Generation → Display
```

## Development

### Project Structure

- `main.py`: Application entry point
- `flow.py`: Flow definitions
- `nodes.py`: Node implementations
- `utils/`: Utility functions
  - `fetch_stock_data.py`: Stock data retrieval
  - `analyze_financials.py`: Financial analysis functions
  - `analyze_sentiment.py`: Sentiment analysis functions
  - etc.

### Adding New Features

To add new features:
1. Implement utility functions in the `utils/` directory
2. Create new node classes in `nodes.py`
3. Update flows in `flow.py` to incorporate the new nodes
4. Update tests to cover the new functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [PocketFlow](https://github.com/the-pocket/PocketFlow)
- Data provided by various financial APIs
