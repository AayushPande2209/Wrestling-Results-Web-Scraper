#!/usr/bin/env python3
"""
Debug script to test scraper with a single wrestler in non-headless mode.
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

def debug_single_wrestler():
    """Debug scraper with a single wrestler from Olentangy Liberty."""
    print("🔍 Debug Mode: Testing single wrestler from Olentangy Liberty")
    print("This will run in visible browser mode for debugging...")
    
    # Initialize scraper in non-headless mode
    scraper = PlaywrightScraper(headless=False)
    
    from playwright.sync_api import sync_playwright
    import time
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Load the page
            scraper._load_page(page)
            
            # Get genders
            genders = scraper._get_genders(page)
            print(f"Found genders: {genders}")
            
            # Select Boys
            scraper._select_gender(page, 'Boys')
            
            # Get schools
            schools = scraper._get_schools(page)
            print(f"Found Liberty schools: {schools}")
            
            # Find Olentangy Liberty specifically
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
            
            # Test with first wrestler
            test_wrestler = wrestlers[0]
            print(f"🤼 Testing with wrestler: {test_wrestler}")
            
            # Select wrestler
            wrestler_selectors = [
                'select[name*="wrestler"]',
                'select[id*="wrestler"]',
                '#wrestler',
                '.wrestler-select',
                'select[name*="athlete"]',
                'select[id*="athlete"]'
            ]
            
            wrestler_selected = False
            for selector in wrestler_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        page.select_option(selector, test_wrestler)
                        page.wait_for_timeout(1000)
                        wrestler_selected = True
                        print(f"✅ Selected wrestler using selector: {selector}")
                        break
                except Exception as e:
                    print(f"❌ Failed to select wrestler with selector {selector}: {e}")
                    continue
            
            if not wrestler_selected:
                print("❌ Could not select wrestler!")
                return
            
            # Pause to let user see the page
            print("🔍 Page loaded. Check the browser window...")
            print("Press Enter to continue with button clicking test...")
            input()
            
            # Try to find and click Get Results button
            print("🔍 Looking for Get Results button...")
            
            # Get all buttons for debugging
            buttons = page.evaluate('''
                Array.from(document.querySelectorAll('input[type="submit"], button')).map(btn => ({
                    tag: btn.tagName,
                    type: btn.type,
                    value: btn.value,
                    text: btn.textContent,
                    id: btn.id,
                    class: btn.className,
                    visible: btn.offsetParent !== null,
                    enabled: !btn.disabled
                }))
            ''')
            
            print("Available buttons:")
            for i, btn in enumerate(buttons):
                print(f"  {i+1}. {btn}")
            
            # Try clicking each button that might be the Get Results button
            result_button_selectors = [
                'input[type="submit"][value*="Results"]',
                'input[type="submit"][value*="Get Results"]',
                'button:has-text("Get Results")',
                'input[value*="Get Results"]',
                'button[value*="Get Results"]',
                '.get-results',
                '#get-results',
                'input[type="submit"]',  # Generic submit button
                'button[type="submit"]'  # Generic submit button
            ]
            
            button_clicked = False
            for selector in result_button_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        is_visible = page.is_visible(selector)
                        is_enabled = page.is_enabled(selector)
                        
                        print(f"🔍 Found button with selector {selector}: visible={is_visible}, enabled={is_enabled}")
                        
                        if is_visible and is_enabled:
                            print(f"🖱️  Clicking button with selector: {selector}")
                            page.click(selector)
                            page.wait_for_load_state('domcontentloaded')
                            time.sleep(3)
                            button_clicked = True
                            print("✅ Button clicked successfully!")
                            break
                        else:
                            print(f"❌ Button not clickable: visible={is_visible}, enabled={is_enabled}")
                except Exception as e:
                    print(f"❌ Failed to click button with selector {selector}: {e}")
                    continue
            
            if not button_clicked:
                print("❌ Could not find or click Get Results button!")
                print("🔍 Manual inspection needed. Check the browser window for the correct button.")
                print("Press Enter to continue...")
                input()
            
            # Check if results loaded
            html_content = page.content()
            print(f"📄 Page content length after button click: {len(html_content)} characters")
            
            # Look for results table
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for tables
            tables = soup.find_all('table')
            print(f"🔍 Found {len(tables)} tables on the page")
            
            for i, table in enumerate(tables):
                text = table.get_text()[:200]  # First 200 chars
                print(f"  Table {i+1}: {text}...")
            
            print("🔍 Debug complete. Check browser window for results.")
            print("Press Enter to close...")
            input()
            
        except Exception as e:
            print(f"❌ Error during debugging: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    debug_single_wrestler()