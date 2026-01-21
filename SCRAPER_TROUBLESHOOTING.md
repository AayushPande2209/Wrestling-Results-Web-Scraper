# Wrestling Analytics Scraper - Troubleshooting Guide

This guide helps resolve common issues when running the wrestling analytics scraper.

## Quick Diagnostics

### 1. Test Your Setup

Run this quick test to verify your setup:

```bash
cd scraper
python -c "
import sys
print('Python version:', sys.version)

try:
    import requests, bs4, supabase
    print('✅ Required packages installed')
except ImportError as e:
    print('❌ Missing package:', e)

try:
    from src.dubstat_scraper import DubStatScraper
    print('✅ Scraper module loads correctly')
except ImportError as e:
    print('❌ Scraper import failed:', e)
"
```

### 2. Test Database Connection

```bash
cd scraper
python -c "
from src.supabase_client import SupabaseClient
try:
    client = SupabaseClient()
    print('✅ Database connection successful')
except Exception as e:
    print('❌ Database connection failed:', e)
"
```

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'src'
ModuleNotFoundError: No module named 'requests'
```

**Solutions:**
1. **Check your directory:**
   ```bash
   pwd  # Should show .../wrestling-analytics-platform/scraper
   cd scraper  # If not in scraper directory
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Use virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Issue 2: Supabase Connection Errors

**Error:**
```
supabase.exceptions.APIError: Invalid API key
supabase.exceptions.APIError: Project not found
```

**Solutions:**
1. **Check environment variables:**
   ```bash
   echo $SUPABASE_URL
   echo $SUPABASE_SERVICE_ROLE_KEY
   ```

2. **Verify Supabase credentials:**
   - Go to your Supabase project dashboard
   - Navigate to Settings > API
   - Copy the correct URL and service role key
   - Update your `.env` file

3. **Test with curl:**
   ```bash
   curl -H "Authorization: Bearer YOUR_SERVICE_ROLE_KEY" \
        -H "apikey: YOUR_ANON_KEY" \
        "YOUR_SUPABASE_URL/rest/v1/wrestlers"
   ```

### Issue 3: No Data Found

**Error:**
```
Scraped 0 matches
Found 0 matches
```

**Solutions:**
1. **Verify tournament URL:**
   - Open the URL in your browser
   - Ensure it shows match results
   - Try a different tournament with known data

2. **Check page structure:**
   ```bash
   curl -s "YOUR_TOURNAMENT_URL" | grep -i "match\|bout\|result"
   ```

3. **Enable debug logging:**
   ```bash
   export LOG_LEVEL=DEBUG
   python run_scraper.py YOUR_URL
   ```

4. **Test with known working URLs:**
   - Look for recent tournaments on DubStat
   - Use tournaments with completed results

### Issue 4: Network/Timeout Errors

**Error:**
```
requests.exceptions.Timeout
requests.exceptions.ConnectionError
```

**Solutions:**
1. **Check internet connection:**
   ```bash
   ping dubstat.com
   curl -I https://www.dubstat.com
   ```

2. **Increase timeout:**
   ```bash
   export SCRAPER_REQUEST_TIMEOUT=60
   ```

3. **Check if DubStat is accessible:**
   - Visit https://www.dubstat.com in browser
   - Try again later if site is down

### Issue 5: Permission/Database Errors

**Error:**
```
psycopg2.errors.InsufficientPrivilege
supabase.exceptions.APIError: permission denied
```

**Solutions:**
1. **Check RLS policies:**
   - Go to Supabase dashboard > Authentication > Policies
   - Ensure service role can insert data
   - Temporarily disable RLS for testing

2. **Verify table structure:**
   ```sql
   -- Run in Supabase SQL editor
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```

3. **Use service role key:**
   - Ensure you're using `SUPABASE_SERVICE_ROLE_KEY`
   - Not the anon key for data insertion

### Issue 6: Data Validation Errors

**Error:**
```
Validation failed
Invalid wrestler name
Invalid score format
```

**Solutions:**
1. **Check data format:**
   ```python
   # Debug individual matches
   from src.dubstat_scraper import DubStatScraper
   scraper = DubStatScraper()
   matches = scraper.scrape_tournament_page(url)
   
   for match in matches[:3]:
       print(f"Wrestler 1: '{match.wrestler1.name}'")
       print(f"Wrestler 2: '{match.wrestler2.name}'")
       print(f"Scores: {match.wrestler1_score}-{match.wrestler2_score}")
   ```

2. **Adjust validation rules:**
   - Edit `src/data_validator.py`
   - Relax validation for testing
   - Check for empty/null values

## Advanced Debugging

### Enable Verbose Logging

```bash
export LOG_LEVEL=DEBUG
export VERBOSE_LOGGING=true
python run_scraper.py YOUR_URL 2>&1 | tee scraper_debug.log
```

### Inspect HTML Structure

```python
import requests
from bs4 import BeautifulSoup

url = "YOUR_TOURNAMENT_URL"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Save HTML for inspection
with open('tournament_page.html', 'w') as f:
    f.write(soup.prettify())

# Look for match data patterns
print("Tables found:", len(soup.find_all('table')))
print("Rows found:", len(soup.find_all('tr')))
```

### Test Individual Components

```python
# Test scraper only
from src.dubstat_scraper import DubStatScraper
scraper = DubStatScraper()
matches = scraper.scrape_tournament_page(url)
print(f"Scraper found: {len(matches)} matches")

# Test validator only
from src.data_validator import DataValidator
validator = DataValidator()
for match in matches:
    is_valid = validator.validate_match_data(match)
    print(f"Match valid: {is_valid}")

# Test database only
from src.supabase_client import SupabaseClient
db = SupabaseClient()
# Try inserting test data
```

## Getting Help

If you're still having issues:

1. **Check the logs:**
   ```bash
   tail -f logs/wrestling_analytics_dev.log
   ```

2. **Create a minimal test case:**
   ```python
   # Save as test_minimal.py
   from src.dubstat_scraper import DubStatScraper
   
   scraper = DubStatScraper()
   url = "YOUR_PROBLEM_URL"
   
   try:
       matches = scraper.scrape_tournament_page(url)
       print(f"Success: {len(matches)} matches")
   except Exception as e:
       print(f"Error: {e}")
       import traceback
       traceback.print_exc()
   ```

3. **Document the issue:**
   - What command you ran
   - Full error message
   - Tournament URL you tried
   - Your environment (OS, Python version)

4. **Check project documentation:**
   - Main README.md
   - scraper/README.md
   - DEPLOYMENT.md

## Environment Checklist

Before running the scraper, verify:

- [ ] Python 3.8+ installed
- [ ] In the `scraper` directory
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables set (`.env` file)
- [ ] Supabase project active and accessible
- [ ] Tournament URL is valid and has data
- [ ] Internet connection working

## Success Indicators

When everything is working correctly, you should see:

```
🏆 Wrestling Analytics Scraper
📄 Scraping: https://www.dubstat.com/tournament/12345
--------------------------------------------------
🔧 Initializing scraper components...
🕷️  Scraping tournament data...
✅ Found 25 matches
🔍 Validating and storing data...
  ✅ Match 1/25: John Smith vs Mike Johnson
  ✅ Match 2/25: Sarah Davis vs Lisa Wilson
  ...
--------------------------------------------------
📊 Summary:
  Total matches found: 25
  Successfully stored: 25
  Validation errors: 0
  Other errors: 0
✅ Scraping completed successfully!
🌐 Check your dashboard to see the new data.
```