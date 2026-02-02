#!/usr/bin/env python3
"""
Playwright-based wrestling analytics scraper.
Usage: python run_scraper.py
"""
import sys
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.playwright_scraper import PlaywrightScraper
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the scraper directory and have installed dependencies:")
    print("  cd scraper")
    print("  pip install -r requirements.txt")
    print("  playwright install chromium")
    sys.exit(1)


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        ]
    )


def main():
    """Main function to run the Playwright scraper."""
    
    print(f"🏆 Wrestling Analytics Scraper (Playwright)")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize scraper
        print("🔧 Initializing Playwright scraper...")
        scraper = PlaywrightScraper(headless=True)  # Set to False for debugging
        
        # Run complete scraping process
        print("🕷️  Starting complete data scraping...")
        print("This will loop through: Gender → School → Wrestler → Results")
        print("⏰ This may take several hours to complete...")
        print()
        
        stats = scraper.scrape_all_data()
        
        # Print summary
        print("-" * 60)
        print("📊 SCRAPING SUMMARY:")
        print(f"  🏫 Total schools processed: {stats['total_schools']}")
        print(f"  🤼 Total wrestlers processed: {stats['total_wrestlers']}")
        print(f"  🥊 Total matches found: {stats['total_matches']}")
        print(f"  ✅ Successfully stored: {stats['successful_inserts']}")
        print(f"  ❌ Errors encountered: {stats['errors']}")
        
        if stats['start_time'] and stats['end_time']:
            duration = stats['end_time'] - stats['start_time']
            print(f"  ⏱️  Total time: {duration}")
        
        success_rate = (stats['successful_inserts'] / max(stats['total_matches'], 1)) * 100
        print(f"  📈 Success rate: {success_rate:.1f}%")
        
        if stats['successful_inserts'] > 0:
            print()
            print("✅ Scraping completed successfully!")
            print("🌐 Check your dashboard to see the new data.")
        else:
            print()
            print("❌ No data was stored. Check the logs for details.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Scraping interrupted by user")
        logger.info("Scraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Scraper failed: {e}")
        logger.error(f"Scraper failed: {e}", exc_info=True)
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Ensure Supabase environment variables are set")
        print("3. Make sure Playwright is installed: playwright install chromium")
        print("4. Check the log file for detailed error information")
        sys.exit(1)


if __name__ == "__main__":
    main()