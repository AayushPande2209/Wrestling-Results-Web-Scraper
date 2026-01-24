#!/usr/bin/env python3
"""
Setup script for the Wrestling Analytics Scraper.
Installs dependencies and sets up Playwright.
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🏆 Wrestling Analytics Scraper Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ Error: requirements.txt not found")
        print("   Make sure you're running this from the scraper directory")
        sys.exit(1)
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("💡 Try using pip3 instead of pip if you have multiple Python versions")
        if not run_command("pip3 install -r requirements.txt", "Installing Python dependencies with pip3"):
            sys.exit(1)
    
    # Install Playwright browsers
    if not run_command("playwright install chromium", "Installing Playwright Chromium browser"):
        print("💡 Make sure Playwright was installed correctly in the previous step")
        sys.exit(1)
    
    # Check environment variables
    print("\n🔍 Checking environment variables...")
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Set these in your .env file or environment:")
        print("   export SUPABASE_URL='your-supabase-url'")
        print("   export SUPABASE_ANON_KEY='your-supabase-anon-key'")
    else:
        print("✅ All required environment variables are set")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Make sure your Supabase environment variables are set")
    print("2. Run the scraper: python run_scraper.py")
    print("3. Or trigger it from the dashboard using the 'Run Scraper' button")
    
    print("\n⚠️  Important notes:")
    print("- The scraper will take several hours to complete")
    print("- It loops through Gender → School → Wrestler → Results")
    print("- Check the log files for detailed progress")

if __name__ == "__main__":
    main()