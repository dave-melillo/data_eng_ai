# Chapter 2 Setup Guide

**Generated:** 2025-07-27 12:41:46
**Chapter:** AI Coding Companions
**Focus:** ChatGPT, prompt engineering, code generation

## Prerequisites

### Software Requirements
- Python 3.8+ installed
- Virtual environment (venv or conda)
- Code editor (VS Code recommended)
- Git for version control

### Account Setup
- OpenAI API account with active API key
- GitHub account for repository access
- Development environment access

### Hardware Requirements
- Minimum 8GB RAM
- Stable internet connection
- 5GB free disk space

## Installation Steps

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-repo/data-eng-ai.git
cd data-eng-ai/ch02

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Create environment file
cp sample.env .env

# Edit .env file with your credentials
nano .env
```

### 3. Verification
```bash
# Test setup
python verify_setup.py

# Run initial examples
jupyter notebook
```

## Chapter-Specific Setup

### Chapter 2 Focus: ChatGPT, prompt engineering, code generation

#### Required APIs
- OpenAI API (GPT-4 access recommended)
- Chapter-specific API endpoints (see chapter content)

#### Dataset Requirements
- Sample datasets provided in setup/ directory
- Instructions for accessing larger datasets

#### Lab Environment
- Jupyter notebooks for interactive examples
- Python scripts for automation examples
- Configuration templates

## Troubleshooting

### Common Issues
1. **API Key Issues**
   - Verify OPENAI_API_KEY in .env file
   - Check API quota and billing status
   - Test with simple API call

2. **Package Installation**
   - Ensure virtual environment is activated
   - Update pip: `pip install --upgrade pip`
   - Check Python version compatibility

3. **Jupyter Issues**
   - Install Jupyter in virtual environment
   - Configure kernel: `python -m ipykernel install --user --name=venv`
   - Restart Jupyter server

### Getting Help
- Check chapter README for specific guidance
- Review error logs in detail
- Consult the main repository documentation
- Open issues on GitHub for persistent problems

## Success Verification

You'll know the setup is successful when:
- ✅ All packages install without errors
- ✅ OpenAI API key tests pass
- ✅ Jupyter notebooks open and run
- ✅ Sample code executes correctly

## Next Steps

After successful setup:
1. Review chapter learning objectives
2. Work through guided examples
3. Complete hands-on lab exercises
4. Experiment with provided datasets

**Setup complete! Ready for Chapter 2 content.**
