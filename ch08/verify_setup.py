#!/usr/bin/env python3
"""
Chapter 8 Setup Verification Script

This script verifies that your environment is properly configured for
the Chapter 8 multi-agent news pipeline notebooks and code listings.

Run from the ch08 directory:
    python verify_setup.py
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print section header"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ️  {text}{RESET}")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} detected")
        print_error("Python 3.8+ is required")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print_header("Checking Python Dependencies")
    
    required_packages = {
        'pandas': '2.0.0',
        'openai': '1.3.0',
        'pydantic': '2.0.0',
        'requests': '2.31.0',
        'python-dotenv': '1.0.0',
        'psycopg': '3.1.0'
    }
    
    optional_packages = {
        'jupyter': '1.0.0',
        'tqdm': '4.65.0'
    }
    
    all_success = True
    
    # Check required packages
    print("Required packages:")
    for package, min_version in required_packages.items():
        try:
            # Handle package name variations
            import_name = package
            if package == 'python-dotenv':
                import_name = 'dotenv'
            
            mod = __import__(import_name)
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{package}: {version}")
        except ImportError:
            print_error(f"{package} not found (required >= {min_version})")
            all_success = False
    
    # Check optional packages
    print("\nOptional packages:")
    for package, min_version in optional_packages.items():
        try:
            mod = __import__(package)
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{package}: {version}")
        except ImportError:
            print_warning(f"{package} not found (optional, recommended for notebooks)")
    
    if not all_success:
        print_error("\nMissing required packages. Install with:")
        print_info("pip install -r requirements.txt")
    
    return all_success

def check_env_files():
    """Check if .env files exist"""
    print_header("Checking Environment Files")
    
    env_locations = [
        Path('notebooks/.env'),
        Path('.env'),
    ]
    
    found_any = False
    for env_path in env_locations:
        if env_path.exists():
            print_success(f"Found: {env_path}")
            found_any = True
        else:
            print_warning(f"Not found: {env_path}")
    
    if not found_any:
        print_error("\nNo .env file found!")
        print_info("Create one from template:")
        print_info("  cp setup/sample.env notebooks/.env")
        print_info("  # Then edit notebooks/.env with your API keys")
        return False
    
    return True

def check_environment_variables():
    """Check if required environment variables are set"""
    print_header("Checking Environment Variables")
    
    # Try to load from .env
    try:
        from dotenv import load_dotenv
        
        # Try loading from different locations
        for env_file in ['.env', 'notebooks/.env']:
            if Path(env_file).exists():
                load_dotenv(env_file)
                print_info(f"Loaded from: {env_file}")
                break
    except ImportError:
        print_warning("python-dotenv not installed, checking system environment only")
    
    required_vars = {
        'NEWS_API_KEY': 'NewsAPI key for article extraction',
        'OPENAI_API_KEY': 'OpenAI API key for AI agents',
        'PGHOST': 'PostgreSQL host (e.g., localhost)',
        'PGPORT': 'PostgreSQL port (e.g., 5432)',
        'PGDATABASE': 'PostgreSQL database name (e.g., news_db)',
        'PGUSER': 'PostgreSQL username (e.g., news_user)',
        'PGPASSWORD': 'PostgreSQL password'
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here' and value != '':
            # Mask sensitive values
            if 'KEY' in var or 'PASSWORD' in var:
                display_value = value[:8] + '...' if len(value) > 8 else '***'
            else:
                display_value = value
            print_success(f"{var}: {display_value}")
        else:
            print_error(f"{var} not set - {description}")
            all_set = False
    
    if not all_set:
        print_error("\nMissing required environment variables!")
        print_info("Edit your .env file with actual values")
        print_info("See setup/sample.env for template")
    
    return all_set

def check_newsapi_connection():
    """Test NewsAPI connection"""
    print_header("Testing NewsAPI Connection")
    
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        load_dotenv('notebooks/.env')
        
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key or api_key == 'your_newsapi_key_here':
            print_error("NEWS_API_KEY not configured")
            return False
        
        # Test API with a simple request
        url = f'https://newsapi.org/v2/everything?q=test&pageSize=1&apiKey={api_key}'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('totalResults', 0)
            print_success(f"NewsAPI connected successfully")
            print_info(f"Test query returned {total} results")
            return True
        elif response.status_code == 401:
            print_error("NewsAPI authentication failed - Invalid API key")
            return False
        elif response.status_code == 426:
            print_error("NewsAPI requires upgrade - You may have hit rate limits")
            print_warning("Free tier: 100 requests/day, last 30 days only")
            return False
        else:
            print_error(f"NewsAPI error: {response.status_code}")
            return False
            
    except ImportError as e:
        print_error(f"Missing dependency: {e}")
        return False
    except Exception as e:
        print_error(f"Connection failed: {e}")
        return False

def check_openai_connection():
    """Test OpenAI API connection"""
    print_header("Testing OpenAI API Connection")
    
    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv()
        load_dotenv('notebooks/.env')
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key.startswith('sk-proj-your'):
            print_error("OPENAI_API_KEY not configured")
            return False
        
        openai.api_key = api_key
        
        # Test API with a simple request
        response = openai.models.list()
        
        print_success("OpenAI API connected successfully")
        print_info(f"Available models: {len(response.data)} models found")
        
        # Check for GPT-4o availability
        models = [m.id for m in response.data]
        if 'gpt-4o' in models:
            print_success("GPT-4o model available")
        else:
            print_warning("GPT-4o not found in available models")
        
        return True
        
    except ImportError as e:
        print_error(f"Missing dependency: {e}")
        return False
    except Exception as e:
        print_error(f"OpenAI connection failed: {e}")
        print_info("Common issues:")
        print_info("  - Invalid API key")
        print_info("  - No billing setup (requires payment method)")
        print_info("  - Usage limits exceeded")
        return False

def check_postgres_connection():
    """Test PostgreSQL connection"""
    print_header("Testing PostgreSQL Connection")
    
    try:
        import psycopg
        from dotenv import load_dotenv
        load_dotenv()
        load_dotenv('notebooks/.env')
        
        # Get connection parameters
        host = os.getenv('PGHOST', 'localhost')
        port = os.getenv('PGPORT', '5432')
        dbname = os.getenv('PGDATABASE', 'news_db')
        user = os.getenv('PGUSER', 'news_user')
        password = os.getenv('PGPASSWORD')
        
        if not password:
            print_error("PGPASSWORD not set in environment")
            return False
        
        # Attempt connection
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=5
        )
        
        # Run test query
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_user, version();")
            db, user_name, version = cur.fetchone()
            
            print_success("PostgreSQL connection successful")
            print_info(f"Database: {db}")
            print_info(f"User: {user_name}")
            print_info(f"Version: {version.split(',')[0]}")
            
            # Check if tables exist
            cur.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                AND tablename IN ('news_articles', 'disney_news_articles');
            """)
            tables = cur.fetchall()
            
            if tables:
                print_info(f"Existing tables: {', '.join([t[0] for t in tables])}")
            else:
                print_info("No pipeline tables yet (will be created on first run)")
        
        conn.close()
        return True
        
    except ImportError as e:
        print_error(f"Missing psycopg package: {e}")
        print_info("Install with: pip install 'psycopg[binary]>=3.1.0'")
        return False
    except Exception as e:
        print_error(f"PostgreSQL connection failed: {e}")
        print_info("\nTroubleshooting steps:")
        print_info("1. Verify PostgreSQL is running")
        print_info("   macOS: brew services list | grep postgresql")
        print_info("   Linux: sudo systemctl status postgresql")
        print_info("2. Verify database exists: psql postgres -c '\\l' | grep news_db")
        print_info("3. Verify user exists: psql postgres -c '\\du' | grep news_user")
        print_info("4. Check connection parameters in .env file")
        print_info("5. See setup/postgres_setup.md for detailed instructions")
        return False

def check_file_structure():
    """Check if required files and directories exist"""
    print_header("Checking File Structure")
    
    required_files = [
        'notebooks/8_guide.ipynb',
        'notebooks/8_lab.ipynb',
        'listing/8_1.py',
        'listing/8_2.py',
        'listing/8_3.py',
        'listing/8_4_8_5.py',
        'setup/postgres_setup.md',
        'setup/sample.env',
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def run_mini_pipeline_test():
    """Run a minimal pipeline test"""
    print_header("Running Mini Pipeline Test")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        load_dotenv('notebooks/.env')
        
        import openai
        from pydantic import BaseModel
        
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Define a simple test schema
        class TestExtraction(BaseModel):
            test_field: str
            test_number: int
        
        # Test structured output
        print_info("Testing AI structured extraction...")
        
        test_prompt = """
        You are a test agent. Return a JSON object with:
        - test_field: "success"
        - test_number: 42
        """
        
        completion = openai.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": test_prompt},
                {"role": "user", "content": "Run test"}
            ],
            response_format=TestExtraction
        )
        
        result = completion.choices[0].message.parsed
        
        if result and result.test_field == "success" and result.test_number == 42:
            print_success("AI agent test passed")
            print_info("Structured extraction working correctly")
            return True
        else:
            print_warning("AI agent test completed but with unexpected results")
            return True
            
    except Exception as e:
        print_error(f"Mini pipeline test failed: {e}")
        print_warning("The pipeline may still work, but verify API keys are correct")
        return False

def print_summary(results):
    """Print summary of all checks"""
    print_header("Setup Verification Summary")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"Total Checks: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    print("\n" + "="*60)
    
    if all(results.values()):
        print(f"\n{GREEN}{BOLD}🎉 ALL CHECKS PASSED!{RESET}")
        print(f"\n{GREEN}You're ready to start Chapter 8!{RESET}\n")
        print("Next steps:")
        print("  1. Open notebooks/8_guide.ipynb for Tesla news pipeline")
        print("  2. Open notebooks/8_lab.ipynb for Disney analytics pipeline")
        print("  3. Run listings: python listing/8_1.py")
        print()
    else:
        print(f"\n{RED}{BOLD}⚠️  SETUP INCOMPLETE{RESET}")
        print(f"\n{RED}Please fix the issues above before proceeding.{RESET}\n")
        print("Common solutions:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Create .env file: cp setup/sample.env notebooks/.env")
        print("  • Set up Postgres: See setup/postgres_setup.md")
        print()
        return False
    
    return True

def main():
    """Run all verification checks"""
    print(f"\n{BOLD}Chapter 8 - Multi-Agent News Pipeline{RESET}")
    print(f"{BOLD}Setup Verification Script{RESET}\n")
    
    # Track results
    results = {}
    
    # Run checks
    results['Python Version'] = check_python_version()
    results['Dependencies'] = check_dependencies()
    results['File Structure'] = check_file_structure()
    results['Environment Files'] = check_env_files()
    results['Environment Variables'] = check_environment_variables()
    results['NewsAPI Connection'] = check_newsapi_connection()
    results['OpenAI Connection'] = check_openai_connection()
    results['PostgreSQL Connection'] = check_postgres_connection()
    results['Pipeline Test'] = run_mini_pipeline_test()
    
    # Print summary
    success = print_summary(results)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

