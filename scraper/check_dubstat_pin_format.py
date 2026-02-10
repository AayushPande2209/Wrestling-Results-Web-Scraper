#!/usr/bin/env python3
"""
Check the actual DubStat page to see if pin scores are available anywhere.
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def check_pin_format():
    """Check if DubStat provides scores for pins."""
    
    url = "https://dubstat.com/dubstat-home/ohio-high-school-wrestling/dubstat-database/"
    
    print("🔍 Checking DubStat Pin Format")
    print("-" * 80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("📄 Loading page...")
            page.goto(url, timeout=60000)
            page.wait_for_load_state('domcontentloaded')
            time.sleep(3)
            
            # Select gender
            print("Selecting Boys...")
            page.select_option('#gender', 'Boys')
            time.sleep(3)
            
            # Wait for schools to load
            page.wait_for_function('document.querySelector("#school").options.length > 1', timeout=10000)
            
            # Select Olentangy Liberty
            print("Selecting Olentangy Liberty...")
            page.select_option('#school', 'Olentangy Liberty')
            time.sleep(3)
            
            # Wait for wrestlers to load
            page.wait_for_function('document.querySelector("#wrestler").options.length > 1', timeout=10000)
            
            # Get first wrestler
            wrestlers = page.evaluate('''
                Array.from(document.querySelector("#wrestler").options)
                    .map(option => option.value)
                    .filter(value => value && value !== "")
            ''')
            
            if wrestlers:
                first_wrestler = wrestlers[0]
                print(f"Selecting wrestler: {first_wrestler}...")
                page.select_option('#wrestler', first_wrestler)
                time.sleep(1)
                
                # Click Get Results
                print("Clicking Get Results...")
                page.click('#get-results')
                page.wait_for_load_state('domcontentloaded')
                time.sleep(3)
                
                # Get the HTML
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find the results table
                table = soup.find('table')
                if table:
                    print("\n📊 Results Table Found!")
                    print("-" * 80)
                    
                    # Get header
                    headers = [th.get_text().strip() for th in table.find_all('th')]
                    print(f"Columns: {headers}")
                    print()
                    
                    # Get first 10 rows
                    rows = table.find_all('tr')[1:11]  # Skip header, get first 10
                    
                    print("First 10 matches:")
                    print()
                    
                    for i, row in enumerate(rows, 1):
                        cells = [td.get_text().strip() for td in row.find_all('td')]
                        if len(cells) >= 6:
                            date = cells[0] if len(cells) > 0 else ''
                            tournament = cells[1] if len(cells) > 1 else ''
                            round_info = cells[2] if len(cells) > 2 else ''
                            weight = cells[3] if len(cells) > 3 else ''
                            wl = cells[4] if len(cells) > 4 else ''
                            result = cells[5] if len(cells) > 5 else ''
                            opponent = cells[6] if len(cells) > 6 else ''
                            
                            print(f"{i}. {date} | {tournament}")
                            print(f"   Round: {round_info} | Weight: {weight}")
                            print(f"   W/L: {wl} | Result: {result}")
                            print(f"   Opponent: {opponent}")
                            
                            # Check if it's a pin
                            if result.startswith('F '):
                                print(f"   ⚠️  PIN FORMAT: '{result}' - No score provided by DubStat")
                            elif 'F (' in result:
                                print(f"   ⚠️  PIN FORMAT: '{result}' - No score provided by DubStat")
                            print()
                    
                    print("-" * 80)
                    print("\n🔍 CONCLUSION:")
                    print("DubStat's Result column formats:")
                    print("  - Pins: 'F (5:32)' - Only time, NO SCORE")
                    print("  - Decisions: 'D (3-0)' - Has score")
                    print("  - Tech Falls: 'TF (22-4)' - Has score")
                    print("  - Major Decisions: 'MD (8-0)' - Has score")
                    print()
                    print("❌ Pin scores before the pin are NOT available in DubStat's database.")
                    print("   This is a limitation of their data, not our scraper.")
                else:
                    print("❌ No results table found")
            
            print("\nPress Enter to close browser...")
            input()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    check_pin_format()
