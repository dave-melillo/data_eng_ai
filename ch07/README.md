# Chapter 7: AI and Advanced Data Transformations

This chapter builds on Chapter 6's data quality techniques by exploring advanced data transformations using both traditional Python methods and AI-driven approaches. The chapter demonstrates how AI can serve as a "multi-spanner" in the data engineering toolkit, simplifying complex transformation tasks through conversational interfaces.

## Chapter Overview

Chapter 7 covers four critical areas of advanced data transformations:

1. **Complex Text Processing with Regular Expressions** - Extracting structured data from unstructured text
2. **Handling Hierarchical and Nested Data Structures** - Flattening JSON and XML data
3. **String Normalization and Entity Resolution** - Identifying duplicate records and matching entities
4. **Time Series and Date-Time Transformations** - Advanced date/time manipulation and business logic

Each section compares traditional Python implementations with AI-powered alternatives, highlighting the advantages and potential pitfalls of each approach.

## Quick Start

**New to this chapter?** Follow these steps to get started quickly:

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure API key**: Copy `sample.env` to `.env` and add your OpenAI API key
3. **Verify setup**: Run `python verify_setup.py` to check everything is working
4. **Start learning**: Open `7_guide.ipynb` in Jupyter or run `python listings/7_1.py`

For detailed setup instructions, see the [Complete Setup Instructions](#complete-setup-instructions) section below.

## Directory Structure

```
ch07/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── sample.env                   # Environment variables template
├── verify_setup.py              # Setup verification script
├── 7_guide.ipynb              # Chapter walkthrough notebook
├── 7_lab.ipynb                # Hands-on lab exercises
├── CH07_Melillo.pdf            # Full manuscript
├── CH07_Melillo.txt            # Text version of manuscript
├── listings/                   # Individual code examples
│   ├── 7_1.py                 # Python regex text processing
│   ├── 7_2.py                 # AI regex text processing
│   ├── 7_3.py                 # Python nested data handling
│   ├── 7_4.py                 # AI nested data handling
│   ├── 7_5.py                 # Python entity resolution
│   ├── 7_6.py                 # AI entity resolution
│   ├── 7_7.py                 # Python time series transformations
│   └── 7_8.py                 # AI time series transformations
├── images/                     # Chapter figures
│   ├── CH07_F01_MELILLO_DATA_AI.png  # Nested JSON structure
│   ├── CH07_F02_MELILLO_DATA_AI.png  # Entity resolution example
│   └── CH07_F03_MELILLO_DATA_AI.png  # Transaction data sample
└── setup/                      # Lab data files
    ├── incoming_customers.json  # Nested customer onboarding data
    ├── crm_customers.csv       # CRM records with duplicates
    └── transactions.csv        # Financial transaction data
```

## Prerequisites

### Technical Prerequisites
- **Python 3.8+** - Required for all exercises and code examples
- **Completion of Chapter 6** - Data Quality and Validation concepts are foundational
- **Basic understanding of regular expressions** - Used in text processing examples
- **Familiarity with pandas DataFrames** - Core data manipulation library
- **JSON/CSV data formats** - Understanding of structured data formats
- **Command line/terminal usage** - For running Python scripts and installing packages

### Knowledge Prerequisites
- **Basic data engineering concepts** - ETL processes, data pipelines
- **Python programming fundamentals** - Functions, classes, error handling
- **Data transformation concepts** - Cleaning, normalization, validation
- **Understanding of APIs** - REST APIs and authentication (for OpenAI integration)

### Account Requirements
- **OpenAI API Account** - Required for AI-powered examples and lab exercises
  - Sign up at: https://platform.openai.com/
  - Requires valid payment method for API usage
  - Estimated cost for chapter exercises: $2-5 USD
- **Jupyter environment** - For interactive notebook exercises (optional but recommended)

## Complete Setup Instructions

### Step 1: Environment Preparation

#### Option A: Using Virtual Environment (Recommended)
```bash
# Navigate to the chapter directory
cd ch07/

# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify Python version (should be 3.8+)
python --version
```

#### Option B: Using Conda
```bash
# Create a new conda environment
conda create -n ch07_data_ai python=3.10

# Activate the environment
conda activate ch07_data_ai

# Navigate to the chapter directory
cd ch07/
```

### Step 2: Install Dependencies

#### Method 1: Using requirements.txt (Recommended)
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(pandas|openai|pydantic|rapidfuzz)"
```

#### Method 2: Manual Installation
```bash
# Core dependencies
pip install pandas>=2.0.0
pip install openai>=1.3.0
pip install python-dotenv>=1.0.0
pip install pydantic>=2.0.0

# Text processing and matching
pip install rapidfuzz>=3.0.0

# Date/time handling
pip install pytz>=2023.3
pip install python-dateutil>=2.8.0

# User interface and progress
pip install tqdm>=4.65.0

# Testing and data generation
pip install faker>=19.0.0

# Jupyter support (optional)
pip install jupyter>=1.0.0
pip install ipykernel>=6.25.0

# Additional utilities (optional)
pip install numpy>=1.24.0
pip install matplotlib>=3.7.0
pip install seaborn>=0.12.0
```

### Step 3: OpenAI API Setup

#### 3.1: Create OpenAI Account and Get API Key
1. **Visit OpenAI Platform**: Go to https://platform.openai.com/
2. **Sign Up/Login**: Create account or login with existing credentials
3. **Add Payment Method**: Go to "Billing" → "Payment methods" and add a valid payment method
4. **Generate API Key**: 
   - Navigate to "API keys" section
   - Click "Create new secret key"
   - Give it a descriptive name (e.g., "Chapter 7 Data Engineering")
   - **IMPORTANT**: Copy the key immediately - you won't be able to see it again
5. **Set Usage Limits** (Recommended):
   - Go to "Billing" → "Usage limits"
   - Set a monthly limit (e.g., $10) to prevent unexpected charges

#### 3.2: Configure Environment Variables
```bash
# Copy the sample environment file
cp sample.env .env

# Edit the .env file with your actual API key
# You can use any text editor:
nano .env
# OR
vim .env
# OR
code .env  # If using VS Code
```

Update the `.env` file with your actual API key:
```env
# Replace 'your_openai_api_key_here' with your actual API key
OPENAI_API_KEY=sk-your-actual-api-key-here
```

#### 3.3: Test API Connection
```bash
# Test the API connection with a simple script
python -c "
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    # Test API connection
    response = openai.models.list()
    print('✅ OpenAI API connection successful!')
    print(f'Available models: {len(response.data)} models found')
except Exception as e:
    print(f'❌ API connection failed: {e}')
    print('Please check your API key and internet connection')
"
```

### Step 4: Verify Setup

#### 4.1: Run Setup Verification Script (Recommended)
```bash
# Run the comprehensive setup verification script
python verify_setup.py

# This script will check:
# - Python version compatibility
# - All required and optional dependencies
# - Environment file configuration
# - OpenAI API connection
# - Data files and code listings
# - Basic functionality tests
```

#### 4.2: Test Traditional Python Examples
```bash
# Test regex processing (no API key required)
python listings/7_1.py

# Test nested data handling (no API key required)
python listings/7_3.py

# Test entity resolution (no API key required)
python listings/7_5.py

# Test time series transformations (no API key required)
python listings/7_7.py
```

#### 4.3: Test AI-Powered Examples
```bash
# Test AI regex processing (requires API key)
python listings/7_2.py

# Test AI nested data handling (requires API key)
python listings/7_4.py

# Test AI entity resolution (requires API key)
python listings/7_6.py

# Test AI time series transformations (requires API key)
python listings/7_8.py
```

#### 4.4: Launch Jupyter Notebooks (Optional)
```bash
# Start Jupyter Lab
jupyter lab

# OR start Jupyter Notebook
jupyter notebook

# Navigate to 7_guide.ipynb or 7_lab.ipynb in the browser
```

### Step 5: Troubleshooting Common Issues

#### API Key Issues
```bash
# Check if .env file exists and has correct format
cat .env

# Verify environment variable is loaded
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print(f'API Key loaded: {key[:10]}...' if key else 'API Key not found')
"
```

#### Dependency Issues
```bash
# Check Python version
python --version

# Check pip version
pip --version

# Upgrade pip if needed
pip install --upgrade pip

# Check installed packages
pip list

# Reinstall specific package if needed
pip uninstall package_name
pip install package_name
```

#### Permission Issues (macOS/Linux)
```bash
# If you get permission errors, try:
pip install --user -r requirements.txt

# Or use sudo (not recommended in virtual environments)
sudo pip install -r requirements.txt
```

### Step 6: Cost Management

#### Understanding OpenAI API Costs
- **GPT-4o Model**: ~$0.005 per 1K input tokens, ~$0.015 per 1K output tokens
- **Estimated chapter cost**: $2-5 USD for all exercises
- **Cost optimization tips**:
  - Use smaller datasets for initial testing
  - Set usage limits in OpenAI dashboard
  - Monitor usage regularly

#### Monitor Usage
```bash
# Check your usage programmatically
python -c "
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    # Note: Usage endpoint may require specific permissions
    print('Check your usage at: https://platform.openai.com/usage')
except Exception as e:
    print(f'Usage check failed: {e}')
"
```

## Key Learning Objectives

By the end of this chapter, you will:

- Master both traditional and AI-driven approaches to complex text processing
- Understand how to flatten hierarchical data structures efficiently
- Implement entity resolution systems for duplicate detection
- Perform advanced time series transformations with business logic
- Recognize when to use AI vs traditional methods for data transformations
- Build comprehensive data pipelines that combine multiple transformation techniques

## Lab Exercises

The lab section (7.5) provides hands-on experience with TheraGPT's messy CRM system, including:

1. **Flattening Nested JSON** - Extract customer data from complex mobile onboarding structures
2. **Complex Text Parsing** - Parse messy address lines and subscription codes
3. **Entity Resolution** - Identify and merge duplicate customer records
4. **Time Series Transformations** - Clean financial data with timezone and business day calculations
5. **Golden Record Creation** - Build comprehensive B2B account profiles

## Key Techniques Demonstrated

### Traditional Python Approaches
- Regex pattern matching with capture groups
- Recursive JSON traversal and flattening
- Fuzzy string matching with rapidfuzz
- Business day calculations with pandas
- Custom fiscal calendar implementations

### AI-Powered Approaches
- Structured response parsing with Pydantic models
- Conversational data extraction prompts
- Flexible entity resolution reasoning
- Natural language transformation instructions
- Adaptive schema handling

## Business Applications

The techniques in this chapter directly apply to:
- **Log Analysis** - Extracting insights from application logs
- **Customer Data Management** - Deduplicating and normalizing customer records
- **Financial Reporting** - Processing transaction data with business rules
- **Data Integration** - Combining data from multiple sources with different formats
- **Accounts Receivable** - Aging analysis and payment term calculations

## Files and Usage

### Listings
Each listing file can be run independently to demonstrate specific techniques:

```bash
# Traditional approaches (no API key required)
python listings/7_1.py  # Regex text processing
python listings/7_3.py  # Nested data flattening
python listings/7_5.py  # Entity resolution
python listings/7_7.py  # Time series transformations

# AI approaches (requires OpenAI API key)
python listings/7_2.py  # AI text processing
python listings/7_4.py  # AI nested data handling
python listings/7_6.py  # AI entity resolution
python listings/7_8.py  # AI time series transformations
```

### Notebooks
- **7_guide.ipynb** - Step-by-step walkthrough of all concepts
- **7_lab.ipynb** - Complete lab exercises with sample data

### Data Files
The `setup/` directory contains realistic sample data for the lab exercises:
- Customer onboarding data with nested structures
- CRM records with intentional duplicates
- Financial transactions requiring complex transformations

## Best Practices

1. **Validation** - Always validate AI-generated transformations against known correct outputs
2. **Error Handling** - Implement robust error handling for both traditional and AI approaches
3. **Performance** - Consider performance implications when choosing between methods
4. **Maintainability** - Use AI for flexibility, traditional methods for predictable patterns
5. **Documentation** - Document transformation logic clearly for future maintenance

## Common Pitfalls

- **AI Hallucinations** - AI may generate plausible but incorrect transformations
- **Over-reliance on AI** - Not all problems require AI; simple regex may suffice
- **Schema Drift** - Changes in data structure may break traditional parsing logic
- **Performance Costs** - AI API calls add latency and cost considerations
- **Validation Gaps** - Insufficient testing of edge cases in transformation logic

## Getting Help

### If You Encounter Issues
1. **Check the troubleshooting section** above for common solutions
2. **Verify your setup** by running the test commands
3. **Review error messages** carefully - they often contain helpful information
4. **Check API usage and billing** at https://platform.openai.com/
5. **Consult the Manning book forums** for community support

### Additional Resources
- **OpenAI Documentation**: https://platform.openai.com/docs
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Python Regular Expressions**: https://docs.python.org/3/library/re.html

## Next Steps

After completing this chapter:
- Practice with your own data transformation challenges
- Experiment with hybrid approaches combining traditional and AI methods
- Explore more advanced Pydantic models for complex data structures
- Consider building reusable transformation pipelines for your organization

For additional support and resources, refer to the Manning book website and community forums. 