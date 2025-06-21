#!/usr/bin/env python3
"""
Chapter 7: AI and Advanced Data Transformations - Setup Verification Script

This script verifies that your environment is properly configured for Chapter 7 exercises.
Run this script after completing the setup instructions in README.md.

Usage: python verify_setup.py
"""

import sys
import os
from pathlib import Path

def print_header(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_status(item, status, details=""):
    """Print a status line with consistent formatting."""
    status_symbol = "✅" if status else "❌"
    print(f"{status_symbol} {item:<40} {details}")

def check_python_version():
    """Check if Python version meets requirements."""
    print_header("Python Version Check")
    
    version = sys.version_info
    required_major, required_minor = 3, 8
    
    is_valid = version.major >= required_major and version.minor >= required_minor
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_status("Python Version", is_valid, f"v{version_str}")
    
    if not is_valid:
        print(f"\n⚠️  Python {required_major}.{required_minor}+ is required. You have {version_str}")
        print("   Please upgrade Python or use a different environment.")
    
    return is_valid

def check_dependencies():
    """Check if all required packages are installed."""
    print_header("Dependencies Check")
    
    required_packages = {
        'pandas': '2.0.0',
        'openai': '1.3.0',
        'python-dotenv': '1.0.0',
        'pydantic': '2.0.0',
        'rapidfuzz': '3.0.0',
        'pytz': '2023.3',
        'python-dateutil': '2.8.0',
        'tqdm': '4.65.0',
        'faker': '19.0.0'
    }
    
    optional_packages = {
        'jupyter': '1.0.0',
        'ipykernel': '6.25.0',
        'numpy': '1.24.0',
        'matplotlib': '3.7.0',
        'seaborn': '0.12.0'
    }
    
    all_packages_ok = True
    
    # Check required packages
    for package, min_version in required_packages.items():
        try:
            if package == 'python-dotenv':
                import dotenv
                version = getattr(dotenv, '__version__', 'unknown')
                module_name = 'dotenv'
            elif package == 'python-dateutil':
                import dateutil
                version = getattr(dateutil, '__version__', 'unknown')
                module_name = 'dateutil'
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                module_name = package
            
            print_status(f"{package} (required)", True, f"v{version}")
            
        except ImportError:
            print_status(f"{package} (required)", False, "Not installed")
            all_packages_ok = False
    
    # Check optional packages
    print("\nOptional packages:")
    for package, min_version in optional_packages.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print_status(f"{package} (optional)", True, f"v{version}")
        except ImportError:
            print_status(f"{package} (optional)", False, "Not installed")
    
    return all_packages_ok

def check_environment_files():
    """Check if environment files exist and are properly configured."""
    print_header("Environment Files Check")
    
    current_dir = Path.cwd()
    sample_env = current_dir / "sample.env"
    env_file = current_dir / ".env"
    
    files_ok = True
    
    # Check sample.env exists
    sample_exists = sample_env.exists()
    print_status("sample.env exists", sample_exists)
    if not sample_exists:
        files_ok = False
    
    # Check .env exists
    env_exists = env_file.exists()
    print_status(".env exists", env_exists)
    
    if env_exists:
        # Check if .env has API key
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                has_api_key = 'OPENAI_API_KEY' in content
                has_placeholder = 'your_openai_api_key_here' not in content
                
                print_status(".env has OPENAI_API_KEY", has_api_key)
                print_status(".env key is configured", has_placeholder)
                
                if not has_api_key:
                    files_ok = False
        except Exception as e:
            print_status(".env readable", False, str(e))
            files_ok = False
    else:
        print("\n⚠️  .env file not found. Please copy sample.env to .env and configure your API key.")
        files_ok = False
    
    return files_ok

def check_openai_connection():
    """Test OpenAI API connection."""
    print_header("OpenAI API Connection Test")
    
    try:
        from dotenv import load_dotenv
        import openai
        
        # Load environment variables
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print_status("API Key loaded", False, "OPENAI_API_KEY not found in environment")
            return False
        
        if api_key == 'your_openai_api_key_here':
            print_status("API Key configured", False, "Still using placeholder value")
            return False
        
        print_status("API Key loaded", True, f"Key: {api_key[:10]}...")
        
        # Test API connection
        openai.api_key = api_key
        response = openai.models.list()
        
        print_status("API Connection", True, f"Found {len(response.data)} models")
        
        # Check for GPT-4o availability
        model_names = [model.id for model in response.data]
        has_gpt4o = 'gpt-4o' in model_names
        print_status("GPT-4o available", has_gpt4o)
        
        return True
        
    except ImportError as e:
        print_status("Required modules", False, f"Import error: {e}")
        return False
    except Exception as e:
        print_status("API Connection", False, f"Error: {e}")
        return False

def check_data_files():
    """Check if required data files exist."""
    print_header("Data Files Check")
    
    setup_dir = Path.cwd() / "setup"
    required_files = [
        "incoming_customers.json",
        "crm_customers.csv", 
        "transactions.csv"
    ]
    
    files_ok = True
    
    print_status("setup/ directory exists", setup_dir.exists())
    
    if setup_dir.exists():
        for filename in required_files:
            file_path = setup_dir / filename
            exists = file_path.exists()
            print_status(f"setup/{filename}", exists)
            if not exists:
                files_ok = False
    else:
        files_ok = False
    
    return files_ok

def check_listings():
    """Check if all listing files exist."""
    print_header("Code Listings Check")
    
    listings_dir = Path.cwd() / "listings"
    required_listings = [f"7_{i}.py" for i in range(1, 9)]
    
    listings_ok = True
    
    print_status("listings/ directory exists", listings_dir.exists())
    
    if listings_dir.exists():
        for filename in required_listings:
            file_path = listings_dir / filename
            exists = file_path.exists()
            print_status(f"listings/{filename}", exists)
            if not exists:
                listings_ok = False
    else:
        listings_ok = False
    
    return listings_ok

def run_basic_tests():
    """Run basic functionality tests."""
    print_header("Basic Functionality Tests")
    
    tests_ok = True
    
    # Test pandas
    try:
        import pandas as pd
        df = pd.DataFrame({'test': [1, 2, 3]})
        print_status("Pandas DataFrame creation", True)
    except Exception as e:
        print_status("Pandas DataFrame creation", False, str(e))
        tests_ok = False
    
    # Test regex
    try:
        import re
        pattern = r'\d+'
        match = re.search(pattern, "test123")
        print_status("Regex processing", True)
    except Exception as e:
        print_status("Regex processing", False, str(e))
        tests_ok = False
    
    # Test Pydantic
    try:
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            name: str
            value: int
        
        model = TestModel(name="test", value=42)
        print_status("Pydantic model creation", True)
    except Exception as e:
        print_status("Pydantic model creation", False, str(e))
        tests_ok = False
    
    return tests_ok

def main():
    """Run all verification checks."""
    print("Chapter 7: AI and Advanced Data Transformations")
    print("Setup Verification Script")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Files", check_environment_files),
        ("OpenAI API", check_openai_connection),
        ("Data Files", check_data_files),
        ("Code Listings", check_listings),
        ("Basic Tests", run_basic_tests)
    ]
    
    results = {}
    for check_name, check_func in checks:
        results[check_name] = check_func()
    
    # Summary
    print_header("Setup Verification Summary")
    
    all_passed = all(results.values())
    
    for check_name, passed in results.items():
        print_status(check_name, passed)
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 All checks passed! Your environment is ready for Chapter 7.")
        print("\nNext steps:")
        print("1. Try running: python listings/7_1.py")
        print("2. Then try: python listings/7_2.py (requires API key)")
        print("3. Open 7_guide.ipynb in Jupyter for interactive learning")
    else:
        print("❌ Some checks failed. Please review the issues above.")
        print("\nTroubleshooting:")
        print("1. Check the README.md for detailed setup instructions")
        print("2. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("3. Verify your .env file has a valid OpenAI API key")
        print("4. Make sure you're in the ch07/ directory")
    
    print(f"{'='*60}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 