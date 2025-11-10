#!/usr/bin/env python3
"""
GraphQA Quick Start Script

This script helps new users get started with GraphQA quickly.
It checks dependencies, guides through setup, and runs a simple test.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Try to load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def print_banner():
    """Print welcome banner"""
    print("🚀 GraphQA Quick Start")
    print("=" * 30)
    print("Welcome to GraphQA - Natural Language Graph Analysis!")
    print("")

def check_python():
    """Check Python version"""
    print("🐍 Checking Python...")
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python {version.major}.{version.minor} found, but 3.8+ required")
        print("   Please upgrade Python: https://python.org")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} (Good!)")
    return True

def check_virtual_env(auto_mode=False):
    """Check if we're in a virtual environment"""
    print("\n📦 Checking virtual environment...")
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  Not in a virtual environment")
        print("   Recommendation: Create one with 'python3 -m venv venv && source venv/bin/activate'")
        if auto_mode:
            print("   Continuing in automated mode...")
            return True
        else:
            response = input("   Continue anyway? (y/N): ").lower()
            if response != 'y':
                return False
    else:
        print("✅ Virtual environment active")
    return True

def check_graphqa_installed():
    """Check if GraphQA is installed"""
    print("\n🔧 Checking GraphQA installation...")
    try:
        import graphqa
        print("✅ GraphQA is installed")
        return True
    except ImportError:
        print("❌ GraphQA not found")
        print("   Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
            print("✅ GraphQA installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install GraphQA")
            print("   Try manually: pip install -e .")
            return False

def check_ollama(auto_mode=False):
    """Check if Ollama is running and gpt-oss:20b model is available"""
    print("\n🤖 Checking Ollama...")

    # Check if Ollama is running
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            print("❌ Ollama is not running")
            print("\n📝 To set up Ollama:")
            print("   1. Install Ollama from https://ollama.ai")
            print("   2. Start Ollama:")
            print("      ollama serve")
            print("   3. Pull the gpt-oss:20b model:")
            print("      ollama pull gpt-oss:20b")

            if auto_mode:
                print("\n   In automated mode - please set up Ollama manually")
                return False

            print("\n   What would you like to do?")
            print("   1. I'll set it up now (exit and restart)")
            print("   2. Skip (I'll set it up later)")

            choice = input("\n   Choose option (1-2): ").strip()
            if choice == "1":
                print("   Please install and start Ollama, then run this script again")
                return False
            else:
                print("   Skipping Ollama setup")
                return False

        # Check if gpt-oss:20b model is available
        model_check = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if "gpt-oss:20b" in model_check.stdout or "gpt-oss" in model_check.stdout:
            print("✅ Ollama is running")
            print("✅ gpt-oss:20b model is available")
            return True
        else:
            print("⚠️  Ollama is running but gpt-oss:20b model not found")
            print("\n📝 To install the model:")
            print("   ollama pull gpt-oss:20b")

            if auto_mode:
                print("\n   In automated mode - please pull the model manually")
                return False

            print("\n   What would you like to do?")
            print("   1. I'll pull the model now (exit and restart)")
            print("   2. Skip (I'll pull it later)")

            choice = input("\n   Choose option (1-2): ").strip()
            if choice == "1":
                print("   Please run 'ollama pull gpt-oss:20b', then run this script again")
                return False
            else:
                print("   Skipping model download")
                return False

    except FileNotFoundError:
        print("❌ curl or ollama command not found")
        print("\n📝 To set up Ollama:")
        print("   1. Install Ollama from https://ollama.ai")
        print("   2. Make sure 'ollama' is in your PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Connection to Ollama timed out")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def run_basic_test():
    """Run a basic functionality test"""
    print("\n🧪 Running basic test...")
    try:
        from graphqa import GraphQA
        print("✅ GraphQA import successful")
        
        # Test initialization (this may fail with dataset loading, which is expected)
        agent = GraphQA(dataset_name="amazon")
        print("✅ Agent initialization successful")
        
        # Note: We don't test dataset loading since sample data may not be available
        print("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n🎉 Quick start completed!")
    print("\n📖 What's next?")
    print("   1. Run the basic example:")
    print("      python examples/basic_usage.py")
    print("")
    print("   2. Verify Ollama is running:")
    print("      ollama list  # Should show gpt-oss:20b model")
    print("      curl http://localhost:11434/api/tags  # Check Ollama API")
    print("")
    print("   3. Customize performance settings:")
    print("      cat config.yaml  # Edit to change dataset loading limits")
    print("      # Templates available:")
    print("      #   cp config-templates/demo.yaml config.yaml (5K products, fast)")
    print("      #   cp config-templates/full-analysis.yaml config.yaml (200K+, slow)")
    print("")
    print("   4. Check documentation:")
    print("      docs/user-guide.md")
    print("")
    print("   5. Try with your own data:")
    print("      - See existing loaders in src/graphqa/loaders/")
    print("      - Create your own data loader")
    print("")
    print("   6. Join the community:")
    print("      - GitHub: https://github.com/catio-tech/graphqa")
    print("      - Issues: https://github.com/catio-tech/graphqa/issues")
    print("")
    print("💡 Tips:")
    print("   - Make sure Ollama is running before using GraphQA")
    print("   - Edit config.yaml to customize dataset loading behavior")
    print("   - We ship in test mode by default to prevent memory overload")

def main():
    """Main quickstart function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GraphQA Setup and Quick Start")
    parser.add_argument("--auto", action="store_true", 
                       help="Run in automated mode (non-interactive)")
    parser.add_argument("--venv", action="store_true",
                       help="Create virtual environment if needed")
    args = parser.parse_args()
    
    # Set global automation mode
    global AUTOMATED_MODE
    AUTOMATED_MODE = args.auto
    
    print_banner()
    
    # Handle venv creation in automated mode
    if args.auto and args.venv:
        create_venv_if_needed()
    
    # Check all requirements
    checks = [
        ("Python version", check_python),
        ("Virtual environment", lambda: check_virtual_env(auto_mode=args.auto)),
        ("GraphQA installation", check_graphqa_installed),
        ("Ollama setup", lambda: check_ollama(auto_mode=args.auto)),
        ("Basic functionality", run_basic_test)
    ]
    
    failed_checks = []
    for name, check_func in checks:
        if not check_func():
            failed_checks.append(name)
    
    if failed_checks:
        print(f"\n❌ Setup incomplete. Failed checks: {', '.join(failed_checks)}")
        if not args.auto:
            print("   Please address the issues above and run this script again.")
        sys.exit(1)
    
    show_next_steps()

def create_venv_if_needed():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("🐍 Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("✅ Virtual environment created")
            print("   Please activate it with: source venv/bin/activate")
            print("   Then run this script again.")
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Global flag for automation mode
    AUTOMATED_MODE = False
    main() 