"""
Chapter 9 - Setup Verification Script

This script verifies that all required dependencies and configurations
are properly set up for Chapter 9.

Run this script to check:
- Python version
- Required packages
- API keys configuration
- Database connectivity
- Docker availability

Usage:
    python verify_setup.py
"""

import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_check(name, status, message=""):
    """Print a check result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if message:
        print(f"   {message}")


def check_python_version():
    """Check Python version is 3.8+"""
    print_header("Python Version")
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 8
    print_check(
        f"Python {version.major}.{version.minor}.{version.micro}",
        is_valid,
        "✓ Compatible" if is_valid else "⚠ Python 3.8+ required"
    )
    return is_valid


def check_packages():
    """Check required packages are installed"""
    print_header("Required Packages")
    
    packages = {
        'pandas': 'pandas',
        'openai': 'openai',
        'psycopg': 'psycopg',
        'pydantic': 'pydantic',
        'requests': 'requests',
        'dotenv': 'python-dotenv',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'scipy': 'scipy',
        'tqdm': 'tqdm',
    }
    
    all_installed = True
    for package, pip_name in packages.items():
        try:
            __import__(package)
            print_check(pip_name, True)
        except ImportError:
            print_check(pip_name, False, f"Install: pip install {pip_name}")
            all_installed = False
    
    return all_installed


def check_environment_variables():
    """Check environment variables are configured"""
    print_header("Environment Configuration")
    
    # Try to load from .env file
    env_file = Path('.env')
    if not env_file.exists():
        print_check(".env file", False, "Run: cp sample.env .env")
        return False
    
    print_check(".env file exists", True)
    
    # Load dotenv if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Check required variables
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key',
        'NEWS_API_KEY': 'NewsAPI key',
        'PGHOST': 'PostgreSQL host',
        'PGDATABASE': 'PostgreSQL database',
        'PGUSER': 'PostgreSQL user',
        'PGPASSWORD': 'PostgreSQL password',
    }
    
    all_configured = True
    for var, description in required_vars.items():
        value = os.getenv(var, '')
        is_set = len(value) > 0 and not value.startswith('your_')
        print_check(
            description,
            is_set,
            f"Set {var} in .env file" if not is_set else ""
        )
        if not is_set:
            all_configured = False
    
    return all_configured


def check_database_connection():
    """Check PostgreSQL connection"""
    print_header("Database Connection")
    
    try:
        import psycopg
        from dotenv import load_dotenv
        load_dotenv()
        
        conn = psycopg.connect(
            host=os.getenv('PGHOST', 'localhost'),
            port=os.getenv('PGPORT', '5432'),
            dbname=os.getenv('PGDATABASE', 'news_db'),
            user=os.getenv('PGUSER', 'news_user'),
            password=os.getenv('PGPASSWORD', ''),
            connect_timeout=5
        )
        
        # Test query
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        print_check("PostgreSQL connection", True)
        print(f"   Version: {version.split(',')[0]}")
        return True
        
    except ImportError:
        print_check("PostgreSQL connection", False, "Install: pip install psycopg[binary]")
        return False
    except Exception as e:
        print_check("PostgreSQL connection", False, f"Error: {str(e)}")
        print("   Check PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD in .env")
        return False


def check_docker():
    """Check Docker is available"""
    print_header("Docker")
    
    import subprocess
    try:
        result = subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            timeout=5
        )
        is_running = result.returncode == 0
        print_check(
            "Docker daemon",
            is_running,
            "Docker is running" if is_running else "Start Docker Desktop"
        )
        return is_running
    except FileNotFoundError:
        print_check("Docker", False, "Install Docker Desktop")
        return False
    except Exception as e:
        print_check("Docker", False, f"Error: {str(e)}")
        return False


def check_api_connections():
    """Check API connections"""
    print_header("API Connections")
    
    # Check OpenAI
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        models = client.models.list()
        print_check("OpenAI API", True, "Connection successful")
    except ImportError:
        print_check("OpenAI API", False, "Install: pip install openai")
    except Exception as e:
        print_check("OpenAI API", False, f"Check API key: {str(e)}")
    
    # Check NewsAPI
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('NEWS_API_KEY')
        response = requests.get(
            'https://newsapi.org/v2/top-headlines',
            params={'country': 'us', 'pageSize': 1, 'apiKey': api_key},
            timeout=5
        )
        
        if response.status_code == 200:
            print_check("NewsAPI", True, "Connection successful")
        else:
            print_check("NewsAPI", False, f"Status: {response.status_code}")
    except ImportError:
        print_check("NewsAPI", False, "Install: pip install requests")
    except Exception as e:
        print_check("NewsAPI", False, f"Check API key: {str(e)}")


def main():
    """Run all verification checks"""
    print("\n" + "🔍 Chapter 9 - Setup Verification")
    
    checks = [
        check_python_version(),
        check_packages(),
        check_environment_variables(),
        check_database_connection(),
        check_docker(),
    ]
    
    # Optional API checks (don't fail on these)
    try:
        check_api_connections()
    except Exception as e:
        print(f"\n⚠️  Could not verify API connections: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed! You're ready to start Chapter 9.")
        print("\nNext steps:")
        print("1. cd airflow_project/")
        print("2. ./quickstart.sh")
        print("3. Open http://localhost:8080")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nFor help, see:")
        print("- README.md")
        print("- airflow_project/SETUP_GUIDE.md")
    
    print("=" * 60 + "\n")
    
    return 0 if all(checks) else 1


if __name__ == '__main__':
    sys.exit(main())

