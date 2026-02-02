#!/usr/bin/env python3
"""
Debug script to test parsing with actual HTML from the site.
This will scrape one wrestler and save the HTML for inspection.
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.playwright_scraper import PlaywrightScraper
from playwright.sync_api import sync_playwright
import time

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def debug_parsing():
    """Debug scraper parsing with one wrestler and save HTML."""
    print("🔍 Debug Mode: Testing parsing with one wrestler")
    print("This will run in visible browser mode and save HTML...")
    
    scraper = PlaywrightScraper(headless=False)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Load the page
            scraper._load_page(page)
            
            # Get genders
            genders = scraper._get_genders(page)
            print(f"Found genders: {genders}")
            
            # Select first gender (usually Boys)
            if genders:
                scraper._select_gender(page, genders[0])
                time.sleep(2)
            
            # Get schools (should filter to Olentangy Liberty)
            schools = scraper._get_schools(page)
            print(f"Found Liberty schools: {schools}")
            
            if not schools:
                print("❌ Olentangy Liberty not found!")
                return
            
            # Select first Olentangy Liberty school
            scraper._select_school(page, schools[0])
            time.sleep(2)
            
            # Get wrestlers
            wrestlers = scraper._get_wrestlers(page)
            print(f"Found {len(wrestlers)} wrestlers at Olentangy Liberty")
            
            if not wrestlers:
                print("❌ No wrestlers found!")
                return
            
            # Test with first wrestler
            test_wrestler = wrestlers[0]
            print(f"🤼 Testing with wrestler: {test_wrestler}")
            
            # Select wrestler and get results
            matches = scraper._scrape_wrestler_results(page, test_wrestler, schools[0])
            
            # Save HTML for inspection
            html_content = page.content()
            with open('debug_html_output.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"💾 Saved HTML to debug_html_output.html")
            
            # Print what we found
            print(f"\n📊 Found {len(matches)} matches")
            for i, match in enumerate(matches, 1):
                print(f"\nMatch {i}:")
                print(f"  Tournament: {match.tournament_name}")
                print(f"  Wrestler1: {match.wrestler1.name}")
                print(f"  Wrestler2: {match.wrestler2.name}")
                print(f"  Winner: {match.winner.name if match.winner else 'None'}")
                print(f"  Score: {match.wrestler1_score}-{match.wrestler2_score}")
                print(f"  Type: {match.match_type.value}")
                print(f"  Round: {match.round}")
            
            if len(matches) == 0:
                print("\n❌ No matches found! This is the issue we need to fix.")
                print("🔍 Check debug_html_output.html to see the actual HTML structure")
            
            print("\nPress Enter to close...")
            input()
            
        except Exception as e:
            print(f"❌ Error during debugging: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    debug_parsing()
