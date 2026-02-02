#!/usr/bin/env python3
"""
Test script to verify data is being inserted into the database correctly.
This will scrape a few wrestlers and check if matches are being stored.
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
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_database_insert():
    """Test that matches are being inserted into the database."""
    print("🧪 Testing Database Insert")
    print("This will scrape 3 wrestlers and verify data is stored...")
    print()
    
    scraper = PlaywrightScraper(headless=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Load the page
            scraper._load_page(page)
            
            # Get genders
            genders = scraper._get_genders(page)
            if not genders:
                print("❌ No genders found!")
                return
            
            # Select first gender
            scraper._select_gender(page, genders[0])
            time.sleep(2)
            
            # Get schools (should filter to Olentangy Liberty)
            schools = scraper._get_schools(page)
            if not schools:
                print("❌ Olentangy Liberty not found!")
                return
            
            print(f"✅ Found school: {schools[0]}")
            scraper._select_school(page, schools[0])
            time.sleep(2)
            
            # Get wrestlers
            wrestlers = scraper._get_wrestlers(page)
            if not wrestlers:
                print("❌ No wrestlers found!")
                return
            
            print(f"✅ Found {len(wrestlers)} wrestlers")
            print()
            
            # Test with first 3 wrestlers
            test_wrestlers = wrestlers[:3]
            total_matches = 0
            total_inserted = 0
            
            for i, wrestler in enumerate(test_wrestlers, 1):
                print(f"🤼 Processing wrestler {i}/{len(test_wrestlers)}: {wrestler}")
                
                try:
                    # Scrape matches
                    matches = scraper._scrape_wrestler_results(page, wrestler, schools[0])
                    print(f"   Found {len(matches)} matches")
                    
                    if matches:
                        # Show first match details
                        match = matches[0]
                        print(f"   Sample match:")
                        print(f"     Tournament: {match.tournament_name}")
                        print(f"     Opponent: {match.wrestler2.name}")
                        print(f"     Winner: {match.winner.name if match.winner else 'None'}")
                        print(f"     Score: {match.wrestler1_score}-{match.wrestler2_score}")
                        print(f"     Type: {match.match_type.value}")
                        print(f"     Round: {match.round}")
                        
                        # Insert into database
                        success = scraper.db_client.batch_insert_matches(matches)
                        if success:
                            print(f"   ✅ Successfully inserted {len(matches)} matches")
                            total_inserted += len(matches)
                        else:
                            print(f"   ❌ Failed to insert matches")
                    
                    total_matches += len(matches)
                    print()
                    
                except Exception as e:
                    print(f"   ❌ Error processing wrestler: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            print("=" * 60)
            print("📊 SUMMARY:")
            print(f"   Total matches found: {total_matches}")
            print(f"   Total matches inserted: {total_inserted}")
            print(f"   Success rate: {(total_inserted/total_matches*100) if total_matches > 0 else 0:.1f}%")
            print()
            
            if total_inserted > 0:
                print("✅ Test passed! Data is being inserted into the database.")
                print("🌐 Check your dashboard to see the new data.")
            else:
                print("❌ Test failed! No data was inserted.")
            
        except Exception as e:
            print(f"❌ Error during test: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    test_database_insert()
