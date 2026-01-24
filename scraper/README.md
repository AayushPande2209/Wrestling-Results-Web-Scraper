# Wrestling Analytics Scraper

A Playwright-based scraper for extracting wrestling match data from DubStat's free results database.

## Overview

This scraper implements the **Gender → School → Wrestler → Results** loop to systematically collect all wrestling match data from Ohio high schools. It uses Playwright for browser automation and BeautifulSoup for HTML parsing.

## Features

- 🎭 **Playwright automation** - Handles dynamic dropdowns and form interactions
- 🔄 **Complete data loop** - Processes all genders, schools, and wrestlers
- 🗄️ **Supabase integration** - Stores data in PostgreSQL database
- 📊 **Dashboard trigger** - Can be started from the web dashboard
- 📝 **Comprehensive logging** - Detailed progress tracking and error handling
- 🛡️ **Data validation** - Cleans and validates extracted data

## Quick Setup

1. **Install dependencies:**
   ```bash
   cd scraper
   python setup.py
   ```

2. **Set environment variables:**
   ```bash
   export SUPABASE_URL="your-supabase-project-url"
   export SUPABASE_ANON_KEY="your-supabase-anon-key"
   ```

3. **Run the scraper:**
   ```bash
   python run_scraper.py
   ```

## How It Works

### Scraping Process

The scraper follows this systematic approach:

1. **Load DubStat database page** (`https://www.dubstat.com/database`)
2. **Loop through genders** (Boys, Girls)
3. **For each gender:**
   - Get all available schools
   - **For each school:**
     - Get all wrestlers at that school
     - **For each wrestler:**
       - Select wrestler from dropdown
       - Click "Get Results" button
       - Parse the results table
       - Extract match data
       - Store in Supabase database

### Data Extracted

From each wrestler's results table:
- Tournament name
- Opponent name and school
- Match result (W/L)
- Score
- Match type (Pin, Decision, Tech Fall, etc.)
- Round information
- Weight class

### Database Storage

Data is stored in three main tables:
- `wrestlers` - Wrestler information
- `tournaments` - Tournament details
- `matches` - Individual match results

## Usage

### Command Line

```bash
# Run complete scraping process
python run_scraper.py

# The scraper will:
# 1. Loop through all genders
# 2. Process all schools for each gender
# 3. Scrape all wrestlers for each school
# 4. Store results in Supabase
```

### Dashboard Integration

The scraper can also be triggered from the web dashboard:

1. Open the dashboard in your browser
2. Click the "Run Scraper" button on the home page
3. The scraper runs in the background
4. Dashboard shows progress and completion status

## Configuration

### Environment Variables

Required environment variables:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

### Scraper Settings

You can modify these settings in `src/playwright_scraper.py`:

- `headless=True` - Run browser in headless mode (set to False for debugging)
- School limit - Currently limited to 50 schools for testing (remove in production)
- Timeouts and wait periods

## Logging

The scraper creates detailed log files:
- Console output shows progress
- Log files saved as `scraper_YYYYMMDD_HHMMSS.log`
- Different log levels for debugging

## Troubleshooting

### Common Issues

1. **"Playwright not found"**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **"Supabase connection failed"**
   - Check your environment variables
   - Verify Supabase URL and key are correct
   - Test connection with: `python -c "from src.supabase_client import SupabaseClient; SupabaseClient().test_connection()"`

3. **"No data found"**
   - Check if DubStat website structure has changed
   - Run with `headless=False` to see browser interactions
   - Check log files for detailed error messages

4. **Scraper stops unexpectedly**
   - Network timeouts are common - scraper will resume from where it left off
   - Check log files for specific error details
   - Restart the scraper to continue

### Debug Mode

To debug scraper issues:

1. Set `headless=False` in `PlaywrightScraper()`
2. Add breakpoints or print statements
3. Check browser developer tools for page structure changes

## Performance

- **Expected runtime:** 4-8 hours for complete Ohio database
- **Data volume:** ~10,000+ wrestlers, ~100,000+ matches
- **Memory usage:** ~100-200MB during operation
- **Network:** Respectful delays between requests

## API Integration

The scraper can be triggered via HTTP API:

```bash
# Start scraper
curl -X POST http://localhost:3000/api/run-scraper

# Response
{
  "success": true,
  "message": "Scraper started successfully",
  "pid": 12345,
  "startTime": "2024-01-15T10:30:00Z"
}
```

## Development

### Project Structure

```
scraper/
├── src/
│   ├── playwright_scraper.py    # Main scraper logic
│   ├── supabase_client.py       # Database operations
│   ├── data_validator.py        # Data validation
│   └── models.py                # Data models
├── run_scraper.py               # Entry point
├── setup.py                     # Setup script
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

### Adding Features

To extend the scraper:

1. **New data fields:** Update `models.py` and parsing logic
2. **Different sites:** Create new scraper class following same interface
3. **Enhanced validation:** Extend `DataValidator` class
4. **Better error handling:** Add try/catch blocks and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Respect DubStat's terms of service and rate limits.