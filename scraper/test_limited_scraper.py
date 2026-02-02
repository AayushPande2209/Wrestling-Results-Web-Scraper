#!/usr/bin/env python3
"""
Test script to run scraper with limited wrestlers from Olentangy Liberty only.
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.playwright_scraper import PlaywrightScraper

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_limited_scraping():
    """Test scraper with just a few wrestlers from Olentangy Liberty."""
    print("🔍 Testing scraper with limited wrestlers from Olentangy Liberty")
    
    # Initialize scraper in headless mode
    scraper = PlaywrightScraper(headless=True)
    
    from playwright.sync_api import sync_playwright
    import time
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Load the page
            scraper._load_page(page)
            
            # Select Boys gender
            scraper._select_gender(page, 'Boys')
            
            # Get schools and find Olentangy Liberty
            schools = scraper._get_schools(page)
            olentangy_liberty = None
            for school in schools:
                if 'olentangy liberty' in school.lower():
                    olentangy_liberty = school
                    break
            
            if not olentangy_liberty:
                print("❌ Olentangy Liberty not found!")
                return
            
            print(f"✅ Found Olentangy Liberty: {olentangy_liberty}")
            
            # Select Olentangy Liberty
            scraper._select_school(page, olentangy_liberty)
            
            # Get wrestlers
            wrestlers = scraper._get_wrestlers(page)
            print(f"Found {len(wrestlers)} wrestlers at Olentangy Liberty")
            
            if not wrestlers:
                print("❌ No wrestlers found!")
                return
            
            # Test with first 3 wrestlers only
            test_wrestlers = wrestlers[:3]
            total_matches = 0
            
            for wrestler in test_wrestlers:
                print(f"🤼 Testing wrestler: {wrestler}")
                
                try:
                    # Scrape this wrestler's results
                    matches = scraper._scrape_wrestler_results(page, wrestler, olentangy_liberty)
                    print(f"✅ Found {len(matches)} matches for {wrestler}")
                    total_matches += len(matches)
                    
                    # Print first match details if any
                    if matches:
                        match = matches[0]
                        print(f"   Sample match: {match.tournament_name} - {match.wrestler1.name} vs {match.wrestler2.name}")
                    
                except Exception as e:
                    print(f"❌ Error processing wrestler {wrestler}: {e}")
                    continue
            
            print(f"\n📊 SUMMARY:")
            print(f"  🤼 Wrestlers tested: {len(test_wrestlers)}")
            print(f"  🥊 Total matches found: {total_matches}")
            print(f"  📈 Average matches per wrestler: {total_matches/len(test_wrestlers):.1f}")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    test_limited_scraping()