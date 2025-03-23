# Stock Analysis Application PRD

## 1. App Overview and Objectives

### 1.1 Executive Summary
The Stock Analysis Application is a comprehensive tool designed for personal use that generates detailed investment reports based on multiple analytical perspectives. Users input a stock ticker symbol, and the application produces an interactive web-based report with graphs and data visualizations that analyze the stock from value investing and technical trading perspectives, compare it with competitors and market segments, and provide investment recommendations.

### 1.2 Core Objectives
- Generate comprehensive stock analysis reports from multiple perspectives
- Provide interactive visualizations with adjustable parameters
- Allow for section-specific report regeneration
- Support persistent notes across reports for the same stock
- Maintain transparency by listing and allowing management of data sources
- Store historical data and documents for future reference using a RAG system
- Offer PDF export functionality for non-interactive report sharing

### 1.3 Success Criteria
- Ability to generate accurate, comprehensive reports for any valid stock ticker
- Interactive charts that correctly display financial data and technical indicators
- Persistent notes that maintain context across multiple report generations
- Effective data retrieval and storage in the RAG system
- Clear, actionable investment insights based on multiple analytical frameworks

## 2. Target Audience

### 2.1 User Profile
The application is designed for personal use by an individual investor who:
- Follows both value investing (Benjamin Graham approach) and technical analysis methodologies
- Requires in-depth analysis before making investment decisions
- Values comprehensive data from multiple perspectives
- Needs to compare potential investments against competitors and market benchmarks
- Uses both web-based interactive reports and static PDFs for analysis

### 2.2 Use Cases
- Analyzing a new potential investment opportunity
- Re-evaluating an existing investment based on new data
- Comparing multiple investment options side by side
- Tracking changes in key metrics over time
- Documenting insights and observations about specific stocks

## 3. Core Features and Functionality

### 3.1 Report Generation

#### 3.1.1 Value Investor Analysis
**Description**: Analyze stocks using Benjamin Graham's value investing approach
**Input**: Stock ticker symbol
**Output**: Analysis section focused on value metrics
**Acceptance Criteria**:
- Calculate and display key value metrics (ROE, P/E, P/B, etc.)
- Identify red flags in company financials
- Analyze company management and board quality
- Identify potentially manipulative actions
- Highlight danger signs in company history

#### 3.1.2 Technical Analysis
**Description**: Provide technical trading analysis with emphasis on price+volume indicators and moving averages
**Input**: Stock ticker symbol, time period (default: 1 year)
**Output**: Technical analysis section with indicators and charts
**Acceptance Criteria**:
- Calculate and display key technical indicators
- Generate multi-timeframe analysis for each indicator
- Emphasize price+volume indicators and moving averages
- Identify key support/resistance levels
- Highlight significant technical patterns

#### 3.1.3 Comparison Analysis
**Description**: Compare stock against competitors, market segment, and overall market
**Input**: Stock ticker symbol
**Output**: Comparative analysis section
**Acceptance Criteria**:
- Identify relevant competitors automatically
- Compare key metrics against competitors
- Generate ratio charts against market segment ETF
- Generate ratio charts against S&P 500 (SPY)
- Identify relative strengths and weaknesses

#### 3.1.4 Investment Recommendation
**Description**: Provide actionable investment recommendation
**Input**: All previous analyses
**Output**: Recommendation section with rationale
**Acceptance Criteria**:
- Generate clear buy/hold/sell recommendation
- Provide confidence level for recommendation
- List key factors supporting recommendation
- Identify potential triggers for changing recommendation
- Compare with other investment opportunities

### 3.2 Interactive Features

#### 3.2.1 Adjustable Graphs
**Description**: Allow interactive adjustment of graph parameters
**Input**: User interactions with graphs
**Output**: Updated visualizations
**Acceptance Criteria**:
- Ability to zoom in/out on time periods
- Toggle visibility of specific indicators
- Change chart types (candlestick, line, etc.)
- Hover for detailed data points
- Download chart images

#### 3.2.2 Persistent Notes
**Description**: Allow adding and storing notes across report generations
**Input**: User-entered notes
**Output**: Notes displayed in context within reports
**Acceptance Criteria**:
- Add notes to specific sections or metrics
- Notes persist when regenerating reports
- Notes are associated with specific stocks
- Edit and delete existing notes
- Notes include timestamps

#### 3.2.3 Section Regeneration
**Description**: Allow regeneration of specific report sections
**Input**: Section selection, optional parameter adjustments
**Output**: Updated report section
**Acceptance Criteria**:
- Regenerate specific sections without full report refresh
- Specify different parameters for regeneration
- Maintain context and notes during regeneration
- Indicate when section was last regenerated
- Compare changes between regenerations

#### 3.2.4 Source Management
**Description**: List and manage data sources used for analysis
**Input**: User inclusion/exclusion of sources
**Output**: Updated report based on selected sources
**Acceptance Criteria**:
- List all sources used in report generation
- Allow including/excluding specific sources
- Indicate confidence level based on sources
- Link to original source when available
- Cache source data in RAG system

### 3.3 Export Functionality

#### 3.3.1 PDF Export
**Description**: Generate static PDF version of the report
**Input**: Current report state
**Output**: Downloadable PDF file
**Acceptance Criteria**:
- Include all report sections and visualizations
- Maintain formatting suitable for printing
- Include notes and annotations
- Timestamps and version information
- Branding and pagination

## 4. Technical Stack Recommendations

### 4.1 Front-end
- **Framework**: React
  - Widely adopted, excellent component ecosystem
  - Good performance for interactive applications
  - Well-supported by visualization libraries
- **Visualization Library**: Plotly.js
  - Extensive financial chart capabilities
  - Support for technical indicators
  - Interactive features built-in
  - Good documentation and community support
- **Styling**: Tailwind CSS
  - Utility-first approach for rapid development
  - Responsive design out-of-the-box
  - Consistent styling across components

### 4.2 Back-end
- **Language**: Python
  - Excellent support for financial analysis
  - Compatible with PocketFlow framework
  - Rich ecosystem of financial libraries
- **Web Framework**: FastAPI
  - High performance, async-capable
  - Good for API development
  - Easy integration with Python-based agents
- **Agent Framework**: PocketFlow
  - As specified by user requirements
  - Good for orchestrating multiple specialized agents
  - Supports flow-based programming model

### 4.3 Data Storage
- **Vector Database**: Qdrant
  - Cost-effective for irregular usage (generous free tier)
  - Supports up to 1M vectors in free tier
  - Good performance for RAG applications
  - Simple API for embedding and retrieval
- **Document Storage**: Local filesystem with Docker volumes
  - For storing generated reports
  - For caching frequently used data

### 4.4 Deployment
- **Containerization**: Docker Compose
  - Multi-container setup for separation of concerns
  - Easily deployable on personal hardware
  - Simplified environment management

## 5. Conceptual Data Model

### 5.1 Shared Store Structure
```python
shared = {
    "input": {
        "ticker": str,             # Stock ticker symbol
        "timestamp": str,          # Report generation time
        "user_params": dict        # User-specified parameters
    },
    "company_info": {
        "name": str,               # Company name
        "sector": str,             # Business sector
        "industry": str,           # Specific industry
        "description": str,        # Business description
        "key_executives": list,    # List of executives and roles
        "founding_date": str       # Company founding date
    },
    "data": {
        "stock_price": {           # Historical price data
            "daily": pandas.DataFrame,
            "weekly": pandas.DataFrame,
            "monthly": pandas.DataFrame
        },
        "financials": {            # Financial statements
            "income_statement": pandas.DataFrame,
            "balance_sheet": pandas.DataFrame,
            "cash_flow": pandas.DataFrame,
            "ratios": pandas.DataFrame
        },
        "competitors": [           # List of competitor data
            {
                "ticker": str,
                "name": str,
                "market_cap": float,
                "key_metrics": dict
            }
        ],
        "market": {                # Market/segment data
            "segment_etf": str,    # Relevant ETF ticker
            "segment_data": pandas.DataFrame,
            "spy_data": pandas.DataFrame,
            "economic_indicators": dict
        }
    },
    "analysis": {
        "value": {                 # Value metrics and analysis
            "metrics": dict,       # Calculated metrics
            "strengths": list,     # Identified strengths
            "weaknesses": list,    # Identified weaknesses
            "red_flags": list,     # Potential warning signs
            "summary": str         # Overall value analysis
        },
        "technical": {             # Technical indicators and analysis
            "indicators": dict,    # Calculated indicators
            "patterns": list,      # Identified patterns
            "support_resistance": list, # Key levels
            "trend_analysis": str, # Trend direction and strength
            "summary": str         # Overall technical analysis
        },
        "comparison": {            # Comparative analysis
            "peer_rankings": dict, # Rankings among peers
            "segment_comparison": dict, # Vs. segment
            "market_comparison": dict,  # Vs. overall market
            "summary": str         # Overall comparison analysis
        },
        "recommendation": {        # Investment recommendation
            "action": str,         # Buy/Hold/Sell
            "confidence": float,   # Confidence level (0-1)
            "rationale": list,     # Key reasons
            "price_targets": dict, # Various scenarios
            "risks": list,         # Key risk factors
            "catalysts": list      # Potential positive triggers
        }
    },
    "rag": {
        "documents": [             # Retrieved relevant documents
            {
                "id": str,
                "title": str,
                "content": str,
                "source": str,
                "date": str,
                "relevance_score": float
            }
        ],
        "sources": [               # Sources used in analysis
            {
                "name": str,
                "type": str,
                "url": str,
                "included": bool,  # User can toggle
                "last_updated": str
            }
        ]
    },
    "report": {
        "sections": {              # Report sections content
            "overview": str,
            "value_analysis": str,
            "technical_analysis": str,
            "comparison": str,
            "recommendation": str,
            "appendix": str
        },
        "visualizations": {        # Generated charts
            "value_charts": dict,
            "technical_charts": dict,
            "comparison_charts": dict
        },
        "notes": {                 # User notes
            "section_id": [
                {
                    "id": str,
                    "content": str,
                    "timestamp": str,
                    "edited": bool
                }
            ]
        },
        "metadata": {              # Report metadata
            "version": str,
            "generated": str,
            "last_updated": str,
            "sections_regenerated": list
        }
    }
}
```

### 5.2 RAG System Implementation

#### 5.2.1 Document Types
- **Company documents**: SEC filings, earnings reports, press releases
- **Market documents**: Industry reports, economic indicators, news articles
- **Analysis documents**: Previous analyses, research reports, expert opinions
- **Technical documents**: Historical technical analyses, pattern records

#### 5.2.2 Vector Collections
- **Stock-specific collection**: Documents relevant to a specific stock
- **Industry collection**: Documents relevant to specific industries
- **Market collection**: Documents about overall market conditions
- **Common collection**: Generally useful documents for any analysis

#### 5.2.3 Document Processing
- Chunking strategy: Split documents by logical sections
- Embedding strategy: Finance-specific embeddings
- Metadata: Store source, date, relevance score, document type

#### 5.2.4 Document Processing Pipeline
```python
pipeline_config = {
    "preprocessing": {
        "text_cleaning": {
            "remove_boilerplate": True,
            "normalize_whitespace": True,
            "handle_special_chars": True
        },
        "language_detection": {
            "minimum_confidence": 0.95,
            "fallback_language": "en"
        }
    },
    "chunking": {
        "strategies": {
            "sec_filings": {
                "method": "semantic_sections",
                "max_tokens": 500
            },
            "news_articles": {
                "method": "paragraph",
                "overlap": 50
            },
            "financial_reports": {
                "method": "table_aware",
                "preserve_tables": True
            }
        }
    },
    "embedding": {
        "model": "finance-bert",
        "dimension": 768,
        "batch_size": 32
    }
}
```

#### 5.2.5 Relevance Scoring
- **Scoring Factors**:
  - Semantic similarity (60%)
  - Temporal relevance (20%)
  - Source reliability (20%)
  - Document type weight

#### 5.2.6 Storage Optimization
```python
collections = {
    "company_specific": {
        "ttl": "90d",
        "update_frequency": "daily",
        "deduplication": True
    },
    "industry_wide": {
        "ttl": "180d",
        "update_frequency": "weekly",
        "deduplication": True
    },
    "market_general": {
        "ttl": "365d",
        "update_frequency": "monthly",
        "deduplication": True
    }
}
```

## 6. UI Design Principles

### 6.1 Overall Layout
- Clean, professional interface with minimal distractions
- Sidebar navigation for quick access to report sections
- Fixed header with report metadata and export options
- Responsive design to accommodate different screen sizes

### 6.2 Report Content
- Clear hierarchy with section headings and subheadings
- Consistent formatting for metrics and indicators
- Color coding for positive/negative values and trends
- Tooltips for explaining complex metrics
- Collapsible sections for managing visual complexity

### 6.3 Visualization Design
- Consistent chart styling across the application
- Color schemes that differentiate between data series
- Clear labeling of axes, data points, and trends
- Interactive elements (zoom, pan, hover tooltips)
- Multiple time frames accessible via tabs
- Toggle controls for showing/hiding indicators

### 6.4 User Interaction
- Intuitive controls for adjusting parameters
- Clear feedback for user actions
- Consistent placement of interactive elements
- Keyboard shortcuts for common actions
- Undo/redo functionality for report modifications

### 6.5 Note System
- Visual distinction between report content and user notes
- Inline note creation and editing
- Note indicators that don't disrupt content flow
- Collapsible note display to manage visual clutter
- Visual indicators for notes that span reports

## 7. Security Considerations

### 7.1 API Key Management
- Store API keys as environment variables in Docker Compose
- Never hardcode API keys in application code
- Implement API key rotation for production use
- Use minimum required permissions for each API

### 7.2 Data Privacy
- Store all data locally within Docker volumes
- Encrypt sensitive data at rest
- Implement secure deletion for outdated data
- No user data sent to external services except for API calls

### 7.3 Network Security
- Restrict web interface to local network
- Use HTTPS for all external API calls
- Implement rate limiting for external API requests
- Log all external data access attempts

### 7.4 Error Handling and Recovery

#### 7.4.1 Data Collection Errors
- **Partial Data Scenarios**:
  | Scenario | Action | User Notification |
  |----------|--------|------------------|
  | Missing price data | Fall back to alternative source | Warning banner |
  | Incomplete financials | Show available periods, highlight gaps | Section notice |
  | Failed technical calculation | Skip indicator, continue others | Indicator-specific message |

- **Recovery Procedures**:
  - Implement exponential backoff for API retries
  - Cache last successful data fetch
  - Provide manual refresh option
  - Log failed attempts for monitoring

#### 7.4.2 Analysis Failures
- **Section-Level Failures**:
  - Isolate failed section
  - Continue processing other sections
  - Provide section regeneration option
  - Cache last successful analysis

#### 7.4.3 User Notification System
- **Notification Levels**:
  - INFO: Non-critical updates
  - WARNING: Degraded functionality
  - ERROR: Section/feature failure
  - CRITICAL: System-wide issues
- **Notification Methods**:
  - In-app notifications
  - Status indicators per section
  - System status dashboard
  - Error logs for debugging

### 7.5 Rate Limiting
```python
rate_limits = {
    "api": {
        "public": {
            "requests_per_minute": 60,
            "requests_per_hour": 1000
        },
        "authenticated": {
            "requests_per_minute": 120,
            "requests_per_hour": 2000
        }
    },
    "data_sources": {
        "yfinance": {
            "requests_per_minute": 30,
            "cooldown_period": "60s"
        },
        "financialdatasets": {
            "requests_per_minute": 50,
            "cooldown_period": "30s"
        }
    }
}
```

### 7.6 Input Validation
- **Validation Rules**:
  ```python
  validation_rules = {
      "ticker": {
          "pattern": "^[A-Z]{1,5}$",
          "blacklist": ["TEST", "DEMO"],
          "sanitization": "uppercase"
      },
      "timeframe": {
          "allowed_values": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y"],
          "default": "1y"
      },
      "indicators": {
          "max_count": 10,
          "allowed_types": ["SMA", "EMA", "RSI", "MACD"]
      }
  }
  ```

### 7.7 Audit Logging
- **Events to Log**:
  - All API requests and responses
  - Data source access
  - Report generation events
  - Configuration changes
  - Security events

## 8. Development Phases and Milestones

### 8.0 Version Control and Development Process
- Use GitHub repository for version control
- Follow Git Flow branching strategy:
  - `main` branch for production releases
  - `develop` branch for ongoing development
  - Feature branches for new functionality
  - Release branches for version preparation
- Implement conventional commit messages for clear change history
- Utilize GitHub Issues for task tracking and bug reporting
- Set up GitHub Actions for automated testing
- Require pull request reviews before merging
- Tag all releases with semantic versioning (MAJOR.MINOR.PATCH)

### 8.1 Phase 1: Foundation and Data Collection (Weeks 1-2)
- Set up project structure following PocketFlow patterns
- Implement Docker Compose configuration
- Create utility functions for data collection from yfinance
- Establish connection to Qdrant for the RAG system
- Implement basic web interface for accepting inputs
- **Milestone**: Ability to input a ticker symbol and fetch basic company data

### 8.2 Phase 2: Core Analysis Features (Weeks 3-5)
- Implement Value Analysis agent (Benjamin Graham approach)
  - Calculate fundamental ratios
  - Analyze company financials
  - Identify red flags
- Implement Technical Analysis agent
  - Calculate technical indicators (price+volume, moving averages)
  - Generate basic charts
- Implement comparison with competitors and market
- **Milestone**: Generate basic analysis for each perspective

### 8.3 Phase 3: Report Generation (Weeks 6-7)
- Design report template structure
- Implement report compilation node
- Create visualization nodes using Plotly.js
- Implement PDF export functionality
- Build interactive web interface for report viewing
- **Milestone**: Generate complete reports with visualizations

### 8.4 Phase 4: Interactive Features and RAG Enhancement (Weeks 8-9)
- Implement notes functionality
- Add ability to regenerate specific sections
- Enhance RAG system with document retrieval
- Implement source management features
- **Milestone**: Fully interactive report with RAG enhancement

### 8.5 Phase 5: Refinement and Optimization (Weeks 10-12)
- Optimize performance of agent workflows
- Enhance visualization interactivity
- Improve error handling and resilience
- Refine report formatting and styling
- Comprehensive testing with various stock types
- **Milestone**: Production-ready application

## 9. Potential Challenges and Solutions

### 9.1 Data Availability Challenge
**Challenge**: Some financial data might not be freely available through yfinance
**Solutions**:
- Implement fallback to financialdatasets.ai API
- Prioritize available metrics and indicators
- Create a clear data sourcing hierarchy
- Add capability to manually input missing data
- Design visualizations to gracefully handle missing data points

### 9.2 Performance Challenge
**Challenge**: Analysis of multiple technical indicators can be computationally intensive
**Solutions**:
- Implement efficient caching strategies
- Use asynchronous calculations where possible
- Prioritize critical indicators for initial loading
- Load additional indicators on demand
- Optimize data structures for repeat calculations

### 9.3 RAG System Challenges
**Challenge**: Effectively embedding and retrieving financial documents
**Solutions**:
- Use finance-specific embedding models when available
- Implement domain-specific chunking strategies
- Create custom relevance scoring for financial documents
- Pre-process common document types (SEC filings, earnings reports)
- Build feedback loop for retrieval quality improvement

### 9.4 Visualization Challenge
**Challenge**: Interactive charts with multiple indicators might be performance-intensive
**Solutions**:
- Implement progressive loading of visualization elements
- Optimize number of data points based on time frame
- Use client-side caching for frequently viewed charts
- Pre-generate static images for common views
- Implement WebWorkers for background processing

### 9.5 Agent Coordination Challenge
**Challenge**: Ensuring multiple specialized agents work together effectively
**Solutions**:
- Define clear interfaces between agents
- Implement robust error handling and fallbacks
- Use a well-structured shared store for data exchange
- Create monitoring and logging for agent activities
- Design agents to be independently testable

## 10. Future Expansion Possibilities

### 10.1 Additional Analysis Perspectives
- Momentum investing analysis
- Growth investing analysis
- Income investing analysis
- ESG (Environmental, Social, Governance) analysis
- Quantitative analysis with machine learning

### 10.2 Advanced Features
- Portfolio analysis across multiple stocks
- Scenario modeling with "what-if" capabilities
- Backtesting of investment strategies
- Custom indicator creation
- Correlation analysis between stocks

### 10.3 Integration Possibilities
- Integration with brokerage APIs for real portfolio data
- RSS/news feed integration for real-time updates
- Economic calendar integration
- Social sentiment analysis from Twitter/Reddit
- Alert system for price/volume breakouts

### 10.4 Accessibility Improvements
- Mobile-responsive design
- Voice command interface
- Customizable report templates
- Scheduled report generation
- Email delivery of reports

## 11. Docker Configuration

### 11.1 Docker Compose Setup
```yaml
version: '3'

services:
  web:
    build: ./web
    ports:
      - "8080:8080"  # Expose to local network
    volumes:
      - ./reports:/app/reports  # Store generated reports
    depends_on:
      - app
    networks:
      - stock-analysis-network

  app:
    build: ./app
    volumes:
      - ./data:/app/data  # Persistent data storage
    environment:
      - QDRANT_API_KEY=${QDRANT_API_KEY}
      - FINANCIALDATASETS_API_KEY=${FINANCIALDATASETS_API_KEY}
    networks:
      - stock-analysis-network

  db-connector:
    build: ./db-connector
    environment:
      - QDRANT_API_KEY=${QDRANT_API_KEY}
    volumes:
      - ./data:/app/data  # Shared with app container
    networks:
      - stock-analysis-network

networks:
  stock-analysis-network:
```

### 11.2 Container-Specific Considerations

#### 11.2.1 Web Container
- **Base Image**: Node.js Alpine
- **Dependencies**: React, Plotly.js, Tailwind CSS
- **Exposed Ports**: 8080
- **Volumes**: Reports directory for generated reports
- **Environment Variables**: API endpoints

#### 11.2.2 App Container
- **Base Image**: Python Alpine
- **Dependencies**: FastAPI, PocketFlow, yfinance, pandas, numpy
- **Volumes**: Data directory for cached data
- **Environment Variables**: API keys, configuration settings

#### 11.2.3 DB Connector Container
- **Base Image**: Python Alpine
- **Dependencies**: Qdrant client, embedding libraries
- **Volumes**: Shared data directory
- **Environment Variables**: Qdrant API key, configuration settings

## 12. Technical Considerations

### 12.1 PocketFlow Implementation

Based on the PocketFlow guide, the application will implement:

#### 12.1.1 Utility Functions
- Located in `/utils` directory
- One file per external API or significant functionality
- Including test functions within each file
- Examples: `fetch_stock_data.py`, `calculate_indicators.py`, `qdrant_client.py`

#### 12.1.2 Node Structure
- Basic structure following the PocketFlow pattern:
  - `prep`: Prepare data from shared store
  - `exec`: Execute core logic
  - `post`: Update shared store with results
- Node types:
  - Regular nodes for sequential processing
  - Batch nodes for parallel processing
  - Async nodes for non-blocking operations

#### 12.1.3 Flow Design
- Defined in separate flow files
- Nodes connected with directional operators (`>>`)
- Conditional branching for different analysis paths
- Error handling and retry logic

### 12.2 RAG Implementation

#### 12.2.1 Document Processing Pipeline
1. Document acquisition (API calls, web scraping)
2. Document preprocessing (cleaning, normalization)
3. Chunking by semantic sections
4. Embedding generation
5. Storage in Qdrant vector database

#### 12.2.2 Retrieval Process
1. Query formation based on analysis context
2. Vector search in appropriate collections
3. Relevance scoring and filtering
4. Context integration into analysis
5. Source tracking for transparency

### 12.3 Visualization Implementation

#### 12.3.1 Chart Types
- Candlestick charts for price data
- Line charts for indicators
- Bar charts for volume
- Heatmaps for correlation matrices
- Radar charts for comparative analysis
- Scatter plots for ratio analysis

#### 12.3.2 Interactive Features
- Zoom and pan controls
- Tooltip information on hover
- Toggle visibility of indicators
- Change timeframes via dropdown
- Annotation capabilities

## 13. Documentation Requirements

### 13.1 User Documentation
- Create comprehensive user documentation with the following components:
  - **Quickstart Guide**: Step-by-step instructions for installation, configuration, and generating the first report
  - **User Manual**: Detailed explanation of all features and how to use them
  - **Wiki**: Comprehensive reference documentation hosted on GitHub
  - **Video Tutorials**: Short screencasts demonstrating key workflows

### 13.2 Technical Documentation
- **Architecture Overview**: Detailed explanation of the application's architecture
- **API Documentation**: Complete documentation of all endpoints with examples
- **Component Documentation**: Explanation of each component's purpose and functionality
- **Configuration Guide**: Instructions for customizing and configuring the application
- **Troubleshooting Guide**: Common issues and their solutions

### 13.3 Documentation Format and Accessibility
- All documentation should be written in Markdown for consistency
- Documentation should be version-controlled alongside the code
- The wiki should be organized with clear navigation and search functionality
- All documentation should be accessible from within the application
- Include screenshots and diagrams where appropriate

## 14. Appendix

### 14.1 Key Libraries and Dependencies

#### 14.1.1 Python Dependencies
- `pocketflow`: Agent orchestration framework
- `yfinance`: Yahoo Finance data access
- `pandas`, `numpy`: Data manipulation
- `fastapi`, `uvicorn`: Web server
- `qdrant-client`: Vector database client
- `sentence-transformers`: Document embedding
- `pdfkit`: PDF generation
- `python-dotenv`: Environment variable management

#### 14.1.2 JavaScript Dependencies
- `react`, `react-dom`: UI framework
- `plotly.js`: Data visualization
- `tailwindcss`: Styling
- `axios`: API requests
- `jspdf`: PDF generation on client side
- `date-fns`: Date manipulation
- `react-query`: Data fetching and caching

### 14.2 API Endpoints

#### 14.2.1 Report Generation
- `POST /api/report/generate`: Generate new report
- `POST /api/report/regenerate`: Regenerate specific section
- `GET /api/report/{ticker}`: Retrieve latest report

#### 14.2.2 Data Access
- `GET /api/data/price/{ticker}`: Get price data
- `GET /api/data/financials/{ticker}`: Get financial data
- `GET /api/data/indicators/{ticker}`: Get technical indicators

#### 14.2.3 Notes Management
- `POST /api/notes`: Create new note
- `PUT /api/notes/{id}`: Update existing note
- `DELETE /api/notes/{id}`: Delete note
- `GET /api/notes/{ticker}`: Get all notes for ticker

#### 14.2.4 Sources Management
- `GET /api/sources/{ticker}`: List all sources
- `PUT /api/sources/toggle/{id}`: Include/exclude source
- `POST /api/sources/add`: Add custom source

### 14.3 Resources and References

#### 14.3.1 Financial Analysis
- Benjamin Graham's Value Investing Principles
- Technical Analysis Resources
- Stock Market Segment Classifications

#### 14.3.2 Technical Implementation
- PocketFlow Documentation
- Qdrant API Documentation
- yfinance API Documentation
- financialdatasets.ai API Documentation
- Plotly.js Financial Charts Documentation

## 15. Performance Optimization

### 15.1 Caching Strategy

#### 15.1.1 Data Caching Rules
- **Price Data**:
  - Cache daily data for 15 minutes
  - Cache weekly/monthly data for 4 hours
  - Store in Redis with TTL
- **Financial Statements**:
  - Cache for 24 hours
  - Update after market hours
  - Force refresh on earnings dates
- **Technical Indicators**:
  - Cache base calculations for 15 minutes
  - Implement progressive loading for charts
  - Store pre-calculated common timeframes

#### 15.1.2 Calculation Optimization
- **Pre-calculation Strategy**:
  - Calculate common technical indicators during off-hours
  - Store results in time-series database
  - Update on significant price changes
- **Real-time Calculations**:
  - Implement WebWorkers for client-side calculations
  - Use streaming updates for price-dependent indicators
  - Batch updates for multiple indicators

#### 15.1.3 Resource Management
- **Memory Management**:
  - Implement LRU cache for frequently accessed stocks
  - Clear old data based on access patterns
  - Monitor memory usage and implement cleanup
- **CPU Optimization**:
  - Distribute heavy calculations across worker processes
  - Implement request queuing for intensive operations
  - Rate limit concurrent calculations

## 16. Testing Strategy

### 16.1 Unit Testing
- **Coverage Requirements**:
  - Minimum 80% code coverage
  - 100% coverage for critical paths
  - All utility functions must be tested
  - All API endpoints must be tested

### 16.2 Integration Testing
```python
test_scenarios = {
    "full_report_generation": {
        "inputs": ["AAPL", "GOOGL", "MSFT"],
        "sections": ["value", "technical", "comparison"],
        "expected_outputs": ["analysis", "charts", "recommendations"]
    },
    "data_source_failover": {
        "primary_source": "yfinance",
        "backup_sources": ["financialdatasets.ai", "alpha_vantage"],
        "validation_points": ["price_data", "financial_statements"]
    },
    "rag_system": {
        "document_types": ["sec_filings", "news", "analysis"],
        "operations": ["indexing", "retrieval", "relevance_scoring"]
    }
}
```

### 16.3 Performance Testing
- **Thresholds**:
  | Operation | Target Time | Max Time |
  |-----------|------------|-----------|
  | Report Generation | 30s | 60s |
  | Section Regeneration | 10s | 20s |
  | Chart Rendering | 2s | 5s |
  | RAG Query | 1s | 3s |

### 16.4 Test Data Management
- **Test Data Sets**:
  - Standard stocks (AAPL, GOOGL, etc.)
  - Edge cases (IPOs, penny stocks)
  - Error cases (delisted stocks)
  - Historical scenarios (market crashes, splits)

### 16.5 Automated Testing Pipeline
```yaml
pipeline:
  stages:
    - lint:
        tools: [pylint, eslint]
        config: ./lint-rules.yml
    - unit_tests:
        runner: pytest
        coverage: pytest-cov
    - integration_tests:
        runner: pytest
        marks: integration
    - performance_tests:
        runner: locust
        scenarios: ./perf-scenarios.yml
    - security_tests:
        tools: [bandit, npm audit]
        config: ./security-rules.yml
```

## 17. Deployment Strategy

### 17.1 Deployment Checklist
```yaml
pre_deployment:
  - Verify all tests passing
  - Check security scan results
  - Validate API documentation
  - Review performance metrics
  - Backup current state

deployment_steps:
  - Stop application containers
  - Apply database migrations
  - Deploy new containers
  - Run health checks
  - Enable traffic

post_deployment:
  - Monitor error rates
  - Check performance metrics
  - Verify data consistency
  - Update documentation
  - Tag release
```

### 17.2 Rollback Procedures
```python
rollback_scenarios = {
    "failed_migration": {
        "detection": "Migration script error",
        "action": "Restore database backup",
        "verification": "Data consistency check"
    },
    "performance_degradation": {
        "detection": "Response time > 2x baseline",
        "action": "Revert to previous container version",
        "verification": "Performance test suite"
    },
    "data_corruption": {
        "detection": "Data validation errors",
        "action": "Restore from last known good state",
        "verification": "Data integrity check"
    }
}
```

### 17.3 CI/CD Pipeline
```yaml
pipeline:
  triggers:
    - push to main
    - pull request
    - scheduled nightly
  
  stages:
    - build:
        - lint
        - test
        - security_scan
    - package:
        - build_containers
        - scan_containers
    - deploy:
        - backup
        - migrate
        - deploy
        - healthcheck
    - monitor:
        - performance
        - errors
        - metrics
```

## 18. API Documentation

### 18.1 Authentication
```python
auth_config = {
    "type": "JWT",
    "expiry": "24h",
    "refresh_window": "1h",
    "rate_limits": {
        "public": "100/hour",
        "authenticated": "1000/hour",
        "premium": "10000/hour"
    }
}

error_responses = {
    401: {"message": "Invalid or expired token"},
    403: {"message": "Insufficient permissions"},
    429: {"message": "Rate limit exceeded"}
}
```

### 18.2 Stock Data Endpoints

#### GET /api/v1/stocks/{ticker}/price
```yaml
parameters:
  - name: ticker
    in: path
    required: true
    schema:
      type: string
      pattern: ^[A-Z]{1,5}$
  - name: interval
    in: query
    schema:
      type: string
      enum: [1m, 5m, 15m, 30m, 1h, 1d]
  - name: range
    in: query
    schema:
      type: string
      enum: [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max]

responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            ticker:
              type: string
            prices:
              type: array
              items:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date-time
                  open:
                    type: number
                  high:
                    type: number
                  low:
                    type: number
                  close:
                    type: number
                  volume:
                    type: integer
```

#### GET /api/v1/stocks/{ticker}/financials
```yaml
parameters:
  - name: ticker
    in: path
    required: true
    schema:
      type: string
      pattern: ^[A-Z]{1,5}$
  - name: statement
    in: query
    required: true
    schema:
      type: string
      enum: [income, balance, cash]
  - name: period
    in: query
    schema:
      type: string
      enum: [quarterly, annual]
      default: annual

responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            ticker:
              type: string
            statement_type:
              type: string
            period:
              type: string
            data:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                  metrics:
                    type: object
                    additionalProperties:
                      type: number
```

### 18.3 Analysis Endpoints

#### POST /api/v1/analysis/technical
```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        properties:
          ticker:
            type: string
            pattern: ^[A-Z]{1,5}$
          indicators:
            type: array
            items:
              type: object
              properties:
                name:
                  type: string
                  enum: [SMA, EMA, RSI, MACD, BB]
                params:
                  type: object
                  additionalProperties: true

responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            ticker:
              type: string
            analysis:
              type: array
              items:
                type: object
                properties:
                  indicator:
                    type: string
                  values:
                    type: array
                    items:
                      type: object
                      properties:
                        timestamp:
                          type: string
                          format: date-time
                        value:
                          type: number
```

#### POST /api/v1/reports/generate
```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        properties:
          ticker:
            type: string
            pattern: ^[A-Z]{1,5}$
          sections:
            type: array
            items:
              type: string
              enum: [overview, financials, technical, news]
          format:
            type: string
            enum: [pdf, html, json]
            default: pdf

responses:
  202:
    description: Report generation started
    content:
      application/json:
        schema:
          type: object
          properties:
            report_id:
              type: string
              format: uuid
            status:
              type: string
              enum: [queued, processing]
            eta_seconds:
              type: integer
```

### 18.4 Websocket API
```yaml
ws_endpoints:
  /ws/v1/price:
    description: Real-time price updates
    message_format:
      type: object
      properties:
        action:
          type: string
          enum: [subscribe, unsubscribe]
        tickers:
          type: array
          items:
            type: string
            pattern: ^[A-Z]{1,5}$
    
  /ws/v1/indicators:
    description: Real-time technical indicator updates
    message_format:
      type: object
      properties:
        action:
          type: string
          enum: [subscribe, unsubscribe]
        ticker:
          type: string
          pattern: ^[A-Z]{1,5}$
        indicators:
          type: array
          items:
            type: string
            enum: [SMA, EMA, RSI, MACD, BB]
```