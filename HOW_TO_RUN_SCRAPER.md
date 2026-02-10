# How to Run the Wrestling Scraper

## Quick Start

```bash
cd scraper
python3 run_scraper.py
```

That's it! The scraper will now:
- ✅ Only scrape Olentangy Liberty Boys (not Girls)
- ✅ Update existing matches with 0-0 scores
- ✅ Skip matches that already have scores
- ✅ Insert new matches that don't exist

---

## What's New (Recent Fixes)

### 1. Boys Only
The scraper now only processes the Boys team, not Girls.

### 2. Smart Updates
No need to delete data anymore! The scraper will:
- Update matches with 0-0 scores
- Skip matches that already have scores
- Insert new matches

### 3. Pin Score Limitation
**Important:** DubStat doesn't provide scores for pins (only the time). This is a limitation of their data, not our scraper. If you need pin scores, use the manual update tool.

---

## Testing Before Running

Check what will be updated:
```bash
cd scraper
python3 test_update_logic.py
```

This shows matches with 0-0 scores that will be updated.

---

## Manual Pin Score Updates (Optional)

If you have pin scores from another source (video, scorebook, etc.):

```bash
cd scraper
python3 update_pin_scores.py
```

This interactive tool lets you manually add scores for pins.

---

## Expected Output

When running the scraper, you'll see:
```
🏆 Wrestling Analytics Scraper (Playwright)
📅 Started: 2026-02-08 21:38:18
------------------------------------------------------------
🔧 Initializing Playwright scraper...
✅ Supabase client initialized successfully
🕷️  Starting complete data scraping...
⏰ This may take several hours to complete...

🏆 Starting complete DubStat scraping...
Loading page: https://dubstat.com/...
Page loaded successfully
Found 2 genders: ['Boys', 'Girls']
Processing only: ['Boys']
🚹 Processing gender: Boys
Found 1 schools for Boys
🏫 Processing school: Olentangy Liberty
Found 51 wrestlers at Olentangy Liberty
🤼 Processing wrestler: [Name]
Found 11 matches for [Name]
Starting batch insert of 11 matches
Updated match scores: [Wrestler1] vs [Wrestler2]...
```

---

## Troubleshooting

### "Invalid URL" Error
Check your `.env` file - make sure URLs start with `https://` (not `yhttps://`)

### "No module named 'playwright'"
Install dependencies:
```bash
cd scraper
pip3 install -r requirements.txt
playwright install chromium
```

### "Supabase URL and key are required"
Make sure your `.env` file has:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-key-here
```

### Scraper Stops or Hangs
- Check your internet connection
- Check the log file for errors
- Try running with `headless=False` to see the browser

---

## How Long Does It Take?

- **Olentangy Liberty Boys:** ~10-15 minutes for 51 wrestlers
- The scraper processes one wrestler at a time
- Progress is saved as it goes (you can stop and restart)

---

## Checking Results

### In Terminal
The scraper shows a summary at the end:
```
📊 SCRAPING SUMMARY:
  🏫 Total schools processed: 1
  🤼 Total wrestlers processed: 51
  🥊 Total matches found: 500+
  ✅ Successfully stored: 500+
  ⏱️  Total time: 0:15:00
```

### In Dashboard
Open your dashboard at `http://localhost:3000` to see the data.

### In Supabase
Check your Supabase dashboard to see the data in the database.

---

## Re-Running the Scraper

You can re-run the scraper anytime:
- It will update matches with 0-0 scores
- It will skip matches that already have scores
- It will add any new matches
- **No need to delete data first!**

---

## Need Help?

1. Check `SCRAPER_FIXES_SUMMARY.md` for detailed fix information
2. Check `scraper/FIXES_IMPLEMENTED.md` for technical details
3. Run `python3 test_update_logic.py` to see what will be updated
4. Check the log files in the scraper directory

---

## Summary

The scraper is now production-ready with:
- ✅ Boys-only filtering
- ✅ Smart update logic
- ✅ No data deletion required
- ✅ Pin time tracking (scores not available from DubStat)

Happy scraping! 🏆
