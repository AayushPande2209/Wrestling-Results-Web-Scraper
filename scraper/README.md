# Wrestling Analytics Scraper

Python-based web scraper for extracting wrestling match data from DubStat and storing it in Supabase.

## Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Supabase project** set up with the wrestling analytics schema
3. **Environment variables** configured (see Configuration section)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd wrestling-analytics-platform
   ```

2. **Navigate to scraper directory**:
   ```bash
   cd scraper
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Set up environment variables** by copying from the root `.env` file or creating a new one:
   ```bash
   cp ../.env .env
   ```

2. **Required environment variables**:
   ```bash
   # Supabase Configuration
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   SUPABASE_ANON_KEY=your-anon-key
   
   # Scraper Configuration
   SCRAPER_USER_AGENT=Mozilla/5.0 (compatible; WrestlingAnalytics/1.0)
   SCRAPER_REQUEST_TIMEOUT=30
   SCRAPER_MAX_RETRIES=3
   SCRAPER_RETRY_DELAY=1
   SCRAPER_BATCH_SIZE=50
   ```

## Manual Scraper Usage

### Method 1: Using the Simple Scraper Script

The easiest way to scrape data is using the simple `scraper.py` script in the root directory:

```bash
# From the root directory
python scraper.py
```

This script will:
- Scrape a hardcoded DubStat tournament URL
- Extract match data
- Print results to console

**To customize the URL**, edit `scraper.py` and change the URL in the script.

### Method 2: Using the Advanced Scraper Module

For more control, use the advanced scraper in the `scraper/src/` directory:

```bash
# From the scraper directory
cd scraper
python -c "
from src.dubstat_scraper import DubStatScraper
from src.supabase_client import SupabaseClient
from src.data_validator import DataValidator

# Initialize components
scraper = DubStatScraper()
db_client = SupabaseClient()
validator = DataValidator()

# Scrape tournament data
url = 'https://www.dubstat.com/tournament/your-tournament-id'
matches = scraper.scrape_tournament_page(url)

# Validate and store data
for match in matches:
    if validator.validate_match_data(match):
        db_client.insert_match(match)

print(f'Successfully processed {len(matches)} matches')
"
```

### Method 3: Interactive Python Session

For testing and exploration:

```bash
cd scraper
python
```

```python
# In Python interactive session
from src.dubstat_scraper import DubStatScraper

# Create scraper instance
scraper = DubStatScraper()

# Scrape a tournament
url = "https://www.dubstat.com/tournament/12345"
matches = scraper.scrape_tournament_page(url)

# Inspect results
print(f"Found {len(matches)} matches")
for match in matches[:3]:  # Show first 3 matches
    print(f"{match.wrestler1.name} vs {match.wrestler2.name}: {match.wrestler1_score}-{match.wrestler2_score}")
```

## Finding Tournament URLs

To find DubStat tournament URLs to scrape:

1. **Visit DubStat.com**
2. **Navigate to tournaments** or search for your team/school
3. **Copy the tournament page URL** (usually in format: `https://www.dubstat.com/tournament/[ID]`)
4. **Use this URL** in any of the scraping methods above

Example URLs:
- `https://www.dubstat.com/tournament/12345`
- `https://www.dubstat.com/results/team/67890`

## Data Storage

The scraper automatically stores data in your Supabase database with these tables:

- **wrestlers**: Individual wrestler information
- **tournaments**: Tournament metadata
- **matches**: Match results and scores

Data is validated before insertion to ensure quality and prevent duplicates.

## Troubleshooting

### Common Issues

#### 1. Import Errors
```
ModuleNotFoundError: No module named 'src'
```
**Solution**: Make sure you're in the `scraper` directory and have installed dependencies:
```bash
cd scraper
pip install -r requirements.txt
```

#### 2. Supabase Connection Errors
```
supabase.exceptions.APIError: Invalid API key
```
**Solution**: Check your environment variables:
- Verify `SUPABASE_URL` is correct
- Ensure `SUPABASE_SERVICE_ROLE_KEY` has proper permissions
- Check that your Supabase project is active

#### 3. No Data Found
```
Scraped 0 matches
```
**Solution**: 
- Verify the tournament URL is correct and accessible
- Check that the tournament page has match results
- Try a different tournament URL
- Check the scraper logs for parsing errors

#### 4. Network Timeouts
```
requests.exceptions.Timeout
```
**Solution**:
- Check your internet connection
- Increase `SCRAPER_REQUEST_TIMEOUT` in environment variables
- Try again later (DubStat might be temporarily unavailable)

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
export LOG_LEVEL=DEBUG
python scraper.py
```

This will show detailed information about:
- HTTP requests and responses
- HTML parsing steps
- Data validation results
- Database insertion attempts

### Testing the Scraper

Test with a known working tournament:

```python
from src.dubstat_scraper import DubStatScraper

scraper = DubStatScraper()
# Use a tournament you know has data
test_url = "https://www.dubstat.com/tournament/test-tournament"
matches = scraper.scrape_tournament_page(test_url)

if matches:
    print("✅ Scraper is working correctly")
    print(f"Found {len(matches)} matches")
else:
    print("❌ No matches found - check URL or page structure")
```

## Advanced Usage

### Batch Processing Multiple Tournaments

```python
from src.dubstat_scraper import DubStatScraper
from src.supabase_client import SupabaseClient

scraper = DubStatScraper()
db_client = SupabaseClient()

tournament_urls = [
    "https://www.dubstat.com/tournament/12345",
    "https://www.dubstat.com/tournament/12346",
    "https://www.dubstat.com/tournament/12347",
]

for url in tournament_urls:
    try:
        matches = scraper.scrape_tournament_page(url)
        for match in matches:
            db_client.insert_match(match)
        print(f"✅ Processed {url}: {len(matches)} matches")
    except Exception as e:
        print(f"❌ Failed to process {url}: {e}")
```

### Custom Data Validation

```python
from src.data_validator import DataValidator

validator = DataValidator()

# Validate individual match
if validator.validate_match_data(match):
    print("✅ Match data is valid")
else:
    print("❌ Match data failed validation")

# Get validation errors
errors = validator.get_validation_errors(match)
for error in errors:
    print(f"Validation error: {error}")
```

## Structure
- `src/` - Main source code
  - `dubstat_scraper.py` - Main scraper class
  - `supabase_client.py` - Database client
  - `data_validator.py` - Data validation
  - `models.py` - Data models
- `config/` - Configuration files
- `requirements.txt` - Python dependencies

## Next Steps

After successfully scraping data:

1. **Verify data in Supabase** - Check your database tables
2. **Test the dashboard** - Ensure scraped data appears in the web interface
3. **Set up regular scraping** - Create a schedule for updating data
4. **Monitor data quality** - Check for any parsing issues or missing data

For dashboard usage, see the main project README and deployment guide.