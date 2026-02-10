#!/usr/bin/env python3
"""
Debug script to inspect DubStat page structure and find correct selectors.
"""
import sys
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def inspect_page():
    """Inspect the DubStat database page to find correct selectors."""
    
    url = "https://dubstat.com/dubstat-home/ohio-high-school-wrestling/dubstat-database/"
    
    print(f"🔍 Inspecting page: {url}")
    print("-" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible browser for debugging
        page = browser.new_page()
        
        try:
            print("📄 Loading page...")
            page.goto(url, timeout=60000)
            page.wait_for_load_state('domcontentloaded')
            time.sleep(5)  # Wait for dynamic content
            
            print("✅ Page loaded successfully\n")
            
            # Get page title
            title = page.title()
            print(f"Page Title: {title}\n")
            
            # Find all select elements
            print("=" * 60)
            print("ALL SELECT ELEMENTS ON PAGE:")
            print("=" * 60)
            
            selects = page.evaluate('''
                Array.from(document.querySelectorAll('select')).map(select => ({
                    id: select.id,
                    name: select.name,
                    className: select.className,
                    options: Array.from(select.options).map(opt => ({
                        value: opt.value,
                        text: opt.text
                    })).slice(0, 10)  // First 10 options only
                }))
            ''')
            
            for i, select in enumerate(selects, 1):
                print(f"\n{i}. SELECT ELEMENT:")
                print(f"   ID: {select['id']}")
                print(f"   Name: {select['name']}")
                print(f"   Class: {select['className']}")
                print(f"   Options (first 10):")
                for opt in select['options']:
                    print(f"      - value='{opt['value']}' text='{opt['text']}'")
            
            # Find all buttons and inputs
            print("\n" + "=" * 60)
            print("ALL BUTTONS AND SUBMIT INPUTS:")
            print("=" * 60)
            
            buttons = page.evaluate('''
                Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"]')).map(btn => ({
                    tag: btn.tagName,
                    id: btn.id,
                    name: btn.name,
                    className: btn.className,
                    type: btn.type,
                    value: btn.value,
                    text: btn.textContent.trim(),
                    visible: btn.offsetParent !== null
                }))
            ''')
            
            for i, btn in enumerate(buttons, 1):
                print(f"\n{i}. {btn['tag']}:")
                print(f"   ID: {btn['id']}")
                print(f"   Name: {btn['name']}")
                print(f"   Class: {btn['className']}")
                print(f"   Type: {btn['type']}")
                print(f"   Value: {btn['value']}")
                print(f"   Text: {btn['text']}")
                print(f"   Visible: {btn['visible']}")
            
            # Find all forms
            print("\n" + "=" * 60)
            print("ALL FORMS:")
            print("=" * 60)
            
            forms = page.evaluate('''
                Array.from(document.querySelectorAll('form')).map(form => ({
                    id: form.id,
                    name: form.name,
                    className: form.className,
                    action: form.action,
                    method: form.method
                }))
            ''')
            
            for i, form in enumerate(forms, 1):
                print(f"\n{i}. FORM:")
                print(f"   ID: {form['id']}")
                print(f"   Name: {form['name']}")
                print(f"   Class: {form['className']}")
                print(f"   Action: {form['action']}")
                print(f"   Method: {form['method']}")
            
            # Save HTML for manual inspection
            html = page.content()
            with open('debug_page_structure.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"\n💾 Full HTML saved to: debug_page_structure.html")
            
            print("\n" + "=" * 60)
            print("🔍 INSPECTION COMPLETE")
            print("=" * 60)
            print("\nKeep the browser open to manually inspect the page.")
            print("Press Enter to close the browser...")
            input()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    inspect_page()
