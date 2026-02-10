# Quick Start Guide - Wrestling Analytics Platform

## 🚀 Running the Scraper

```bash
cd scraper
python3 run_scraper.py
```

**What it does:**
- ✅ Scrapes Olentangy Liberty Boys only (not Girls)
- ✅ Updates existing matches with 0-0 scores
- ✅ Skips matches that already have scores
- ✅ Inserts new matches
- ✅ Captures pin times (e.g., "5:32")

## 📊 Running the Dashboard

```bash
cd dashboard
npm run dev
```

Then open: http://localhost:3000

**What you'll see:**
- ✅ Pin matches show time (e.g., "5:32") instead of "0-0"
- ✅ Other matches show scores normally (e.g., "3-0")
- ✅ Wrestler profiles with match history
- ✅ Tournament results and statistics

## 🔧 Testing

### Test Scraper Update Logic:
```bash
cd scraper
python3 test_update_logic.py
```

### Check Pin Format on DubStat:
```bash
cd scraper
python3 check_dubstat_pin_format.py
```

### Manual Pin Score Updates (if needed):
```bash
cd scraper
python3 update_pin_scores.py
```

## 📝 Key Files

### Scraper:
- `scraper/run_scraper.py` - Main scraper entry point
- `scraper/src/playwright_scraper.py` - Scraping logic
- `scraper/src/supabase_client.py` - Database operations

### Dashboard:
- `dashboard/src/app/wrestlers/[id]/page.tsx` - Wrestler profiles
- `dashboard/src/app/tournaments/[id]/page.tsx` - Tournament details
- `dashboard/src/types/database.ts` - TypeScript types

### Configuration:
- `.env` - Environment variables (Supabase credentials)
- `scraper/requirements.txt` - Python dependencies
- `dashboard/package.json` - Node.js dependencies

## 🎯 Recent Changes

### ✅ Scraper Fixes:
1. **Boys Only** - No longer scrapes Girls team
2. **Smart Updates** - Updates 0-0 matches, skips matches with scores
3. **No Deletion Needed** - Can re-run without deleting data

### ✅ Dashboard Updates:
1. **Pin Display** - Shows pin time (e.g., "5:32") instead of "0-0"
2. **Accurate Data** - Reflects what DubStat actually provides
3. **Better UX** - More informative for users

## 📖 Documentation

- `SCRAPER_FIXES_SUMMARY.md` - Detailed scraper fixes
- `PIN_SCORES_EXPLANATION.md` - Why pins show 0-0 in database
- `DASHBOARD_PIN_DISPLAY_UPDATE.md` - Dashboard changes
- `IMPLEMENTATION_COMPLETE.md` - Complete implementation summary
- `HOW_TO_RUN_SCRAPER.md` - Detailed scraper usage

## ⚠️ Important Notes

### Pin Scores:
- DubStat doesn't provide scores before pins
- Only provides pin time (e.g., "5:32")
- This is a DubStat limitation, not a scraper bug
- Dashboard now shows pin time instead of 0-0

### Environment Variables:
Make sure `.env` has:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key
```

### Dependencies:
```bash
# Python (scraper)
cd scraper
pip3 install -r requirements.txt
playwright install chromium

# Node.js (dashboard)
cd dashboard
npm install
```

## 🐛 Troubleshooting

### Scraper Issues:
- Check `.env` file has correct Supabase credentials
- Ensure Playwright is installed: `playwright install chromium`
- Check internet connection
- View logs in `scraper/scraper_*.log`

### Dashboard Issues:
- Check environment variables in `.env`
- Ensure Supabase is accessible
- Check browser console for errors
- Verify data exists in Supabase

## 🎉 You're All Set!

Everything is configured and ready to use. Just run the scraper to collect data, then view it in the dashboard!
