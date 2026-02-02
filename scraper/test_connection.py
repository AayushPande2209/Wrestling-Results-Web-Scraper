#!/usr/bin/env python3
"""
Simple test to check if we can access DubStat website.
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from playwright.sync_api import sync_playwright

def test_dubstat_access():
    """Test if we can access the DubStat website."""
    print("🧪 Testing DubStat website access...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run with visible browser
        page = browser.new_page()
        
        try:
            print("📡 Attempting to load https://dubstat.com...")
            page.goto("https://dubstat.com", timeout=30000)
            
            title = page.title()
            print(f"✅ Successfully loaded page: {title}")
            
            # Try to access the database page
            print("📡 Attempting to load Ohio wrestling database page...")
            page.goto("https://dubstat.com/dubstat-home/ohio-high-school-wrestling/dubstat-database/", timeout=30000)
            
            title = page.title()
            print(f"✅ Successfully loaded database page: {title}")
            
            # Take a screenshot for debugging
            page.screenshot(path="dubstat_screenshot.png")
            print("📸 Screenshot saved as dubstat_screenshot.png")
            
            # Wait a bit so we can see the page
            input("Press Enter to continue...")
            
        except Exception as e:
            print(f"❌ Failed to access DubStat: {e}")
            
            # Try to get any content that did load
            try:
                content = page.content()[:500]  # First 500 chars
                print(f"Page content preview: {content}")
            except:
                pass
                
        finally:
            browser.close()

if __name__ == "__main__":
    test_dubstat_access()