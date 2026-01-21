#!/usr/bin/env python3
"""
Simple script to run the wrestling analytics scraper.
Usage: python run_scraper.py [tournament_url]
"""
import sys
import os
from typing import Optional

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from dubstat_scraper import DubStatScraper
    from supabase_client import SupabaseClient
    from data_validator import DataValidator
    from models import MatchData
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the scraper directory and have installed dependencies:")
    print("  cd scraper")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main function to run the scraper."""
    
    # Get tournament URL from command line or use default
    if len(sys.argv) > 1:
        tournament_url = sys.argv[1]
    else:
        # Default test URL - replace with a real tournament URL
        tournament_url = "https://www.dubstat.com/tournament/example"
        print(f"No URL provided, using default: {tournament_url}")
        print("Usage: python run_scraper.py <tournament_url>")
        print()
    
    print(f"🏆 Wrestling Analytics Scraper")
    print(f"📄 Scraping: {tournament_url}")
    print("-" * 50)
    
    try:
        # Initialize components
        print("🔧 Initializing scraper components...")
        scraper = DubStatScraper()
        db_client = SupabaseClient()
        validator = DataValidator()
        
        # Scrape tournament data
        print("🕷️  Scraping tournament data...")
        matches = scraper.scrape_tournament_page(tournament_url)
        
        if not matches:
            print("❌ No matches found. Check the URL or try a different tournament.")
            return
        
        print(f"✅ Found {len(matches)} matches")
        
        # Validate and store data
        print("🔍 Validating and storing data...")
        successful_inserts = 0
        validation_errors = 0
        
        for i, match in enumerate(matches, 1):
            try:
                # Validate match data
                if validator.validate_match_data(match):
                    # Insert into database
                    db_client.insert_match(match)
                    successful_inserts += 1
                    print(f"  ✅ Match {i}/{len(matches)}: {match.wrestler1.name} vs {match.wrestler2.name}")
                else:
                    validation_errors += 1
                    print(f"  ❌ Match {i}/{len(matches)}: Validation failed")
                    
            except Exception as e:
                print(f"  ❌ Match {i}/{len(matches)}: Error - {e}")
                continue
        
        # Summary
        print("-" * 50)
        print(f"📊 Summary:")
        print(f"  Total matches found: {len(matches)}")
        print(f"  Successfully stored: {successful_inserts}")
        print(f"  Validation errors: {validation_errors}")
        print(f"  Other errors: {len(matches) - successful_inserts - validation_errors}")
        
        if successful_inserts > 0:
            print("✅ Scraping completed successfully!")
            print("🌐 Check your dashboard to see the new data.")
        else:
            print("❌ No data was stored. Check the troubleshooting guide.")
            
    except Exception as e:
        print(f"❌ Scraper failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify the tournament URL is correct")
        print("3. Ensure Supabase environment variables are set")
        print("4. Try running with DEBUG logging: export LOG_LEVEL=DEBUG")
        sys.exit(1)


if __name__ == "__main__":
    main()