# Chapter 10: The Manual Web Scraping Challenge

This chapter introduces web scraping fundamentals and demonstrates why manual extraction doesn't scale, setting up the motivation for AI-powered solutions in subsequent chapters.

## Chapter Overview

Chapter 10 focuses on understanding the data enrichment problem by doing it the hard way first:

1. **The RuckZone Use Case** - Building a product database for an outdoor gear company
2. **Pipeline Overview** - The 6-stage enrichment pipeline we'll build across Part 3
3. **Data Preparation** - Loading products and creating search keys
4. **Web Scraping Fundamentals** - HTTP requests and HTML parsing with Python
5. **The Extraction Challenge** - Why CSS selectors break and manual approaches fail
6. **The Case for AI** - Setting up the motivation for Chapters 11-13

## Quick Start

**New to this chapter?** Follow these steps to get started quickly:

1. **Install dependencies**:
   ```bash
   cd ch10/
   pip install -r requirements.txt
   ```

2. **Configure environment** (optional for this chapter):
   ```bash
   cp sample.env .env
   # Edit .env with your OpenAI API key (needed in later chapters)
   ```

3. **Launch Jupyter**:
   ```bash
   jupyter lab notebooks/
   # Open 10_guide_x.ipynb for the chapter walkthrough
   # Open 10_lab_x.ipynb for hands-on exercises
   ```

## Directory Structure

```
ch10/
├── README.md                    # This file
├── notebooks/
│   ├── 10_guide_x.ipynb        # Chapter walkthrough
│   ├── 10_lab_x.ipynb          # Hands-on lab exercises
│   └── rucking_camping_products.xlsx  # Source data (also in data/)
├── data/
│   ├── README.md               # Data file documentation
│   └── rucking_camping_products.xlsx  # Source product data
├── listings/                    # Individual code examples
│   └── (code listings to be added)
├── requirements.txt             # Python dependencies
└── sample.env                   # Environment variables template
```

## Prerequisites

### Technical Prerequisites
- **Python 3.8+** - Required for all exercises
- **Basic Python knowledge** - Functions, loops, data structures
- **Familiarity with pandas** - DataFrames and basic operations

### Knowledge Prerequisites
- **HTTP basics** - Understanding requests and responses
- **HTML fundamentals** - Tags, attributes, document structure
- **Data transformation concepts** - From prior chapters

## Key Learning Objectives

By the end of this chapter, you will:

- Understand the product enrichment use case and target schema
- Load and prepare source data for the enrichment pipeline
- Make HTTP requests to fetch web pages with Python
- Parse and clean HTML using BeautifulSoup
- Attempt manual data extraction and experience its limitations
- Understand why AI-powered extraction is necessary

## The 6-Stage Pipeline

This chapter introduces the enrichment pipeline we'll build across Part 3:

| Stage | Description | Chapter |
|-------|-------------|---------|
| 1 | Data Preparation | 10 |
| 2 | URL Discovery | 11 |
| 3 | HTML Fetching | 10, 11 |
| 4 | Image Extraction | 12 |
| 5 | AI-Powered Extraction | 12 |
| 6 | Target Mapping & Validation | 13 |

## Source Data

The chapter uses `rucking_camping_products.xlsx`:

- **~445 products** across multiple categories
- **Simple structure**: Brand Name + Product Name
- **Categories**: Backpacks, tents, sleeping bags, pads, stoves, water filters, headlamps

Example products:
- GORUCK GR1 26L
- Osprey Atmos AG 65
- MSR Hubba Hubba 2
- Big Agnes Copper Spur HV UL2

## Key Concepts

### Web Scraping Basics
- HTTP GET requests with the `requests` library
- HTML parsing with BeautifulSoup
- Cleaning HTML by removing scripts, styles, and navigation
- Extracting text content from elements

### The Extraction Challenge
- Sites block automated requests
- JavaScript-rendered content is invisible to basic scrapers
- CSS selectors break across different sites
- Data formats vary (weight: "1.5 lbs", "24 oz", "680g")
- Fields may be missing or ambiguous

### Why Manual Doesn't Scale
- Each site requires custom extraction code
- Maintenance burden grows with each new source
- Edge cases multiply exponentially
- Human time is the bottleneck

## Lab Exercises

The lab provides hands-on experience with:

1. **Data Loading** - Load the Excel file and create search keys
2. **Web Page Fetching** - Retrieve product pages with requests
3. **HTML Parsing** - Clean and extract content with BeautifulSoup
4. **Extraction Attempts** - Try to pull structured data from real pages
5. **Document Failures** - Record what works and what doesn't

## Common Issues

### Blocked Requests
Many sites block requests without browser-like headers:
```python
headers = {'User-Agent': 'Mozilla/5.0 (compatible; educational-bot)'}
response = requests.get(url, headers=headers)
```

### Timeout Errors
Always set reasonable timeouts:
```python
response = requests.get(url, timeout=10)
```

### JavaScript Content
Content loaded via JavaScript won't appear in `requests` responses. This is one reason we need more sophisticated approaches.

## Related Chapters

- **Chapter 11** - URL Discovery with Search APIs
- **Chapter 12** - AI-Powered Data Extraction
- **Chapter 13** - Building the Complete Pipeline

## Next Steps

After completing this chapter:

1. Review the pipeline overview diagram
2. Understand the target schema fields
3. Experience the pain of manual extraction
4. Prepare for automated URL discovery in Chapter 11

---

**Ready to begin?** Open `notebooks/10_guide_x.ipynb` and follow along with the chapter!
