# Implementation Plan: Wrestling Analytics MVP (Simplified)

## Overview

This is a **true MVP** focused on shipping a working wrestling analytics system. The approach prioritizes core functionality over enterprise features. 

**Core Philosophy**: If you can't finish a feature in 1 sitting, it's not MVP.

**MVP Goal**: Answer "Can I see wrestling stats for my teammates?" - Not "Can I build TrackWrestling 2.0?"

## Development Phases

### Phase 1: Data Pipeline ✅ COMPLETE
Scrape DubStat → Store in Supabase → Normalize matches

### Phase 2: Simple Stats ✅ COMPLETE  
Calculate basic wrestling statistics only

### Phase 3: Dashboard (2 pages only)
Build minimal web interface

### Phase 4: Deploy & Ship
Deploy to Vercel, connect Supabase, manual scraper

## Tasks

### Phase 1: Data Pipeline ✅ COMPLETE

- [x] 1. Set up Supabase database
  - ✅ Supabase project created with full schema
  - ✅ All tables created (teams, wrestlers, tournaments, matches, scraper_jobs)
  - ✅ Foreign key constraints and indexes
  - ✅ Environment configuration template
  - _Requirements: 2_

- [x] 2. Build basic Python scraper
  - [x] 2.1 Create simple scraper script
    - ✅ Complete DubStatScraper class with BeautifulSoup
    - ✅ HTML parsing for tournament pages
    - ✅ Data extraction for wrestlers, teams, scores, matches
    - ✅ Basic scraper.py script
    - _Requirements: 1_

  - [x] 2.2 Add data validation
    - ✅ Complete DataValidator class
    - ✅ Validation for names, scores, weight classes
    - ✅ Data cleaning and normalization
    - ✅ Error logging and graceful handling
    - _Requirements: 5_

  - [x] 2.3 Connect to Supabase
    - ✅ Complete SupabaseClient class
    - ✅ Batch insertion with duplicate prevention
    - ✅ Full CRUD operations for all entities
    - ✅ Error handling and logging
    - _Requirements: 2_

- [x] 3. Test data pipeline
  - ✅ All components implemented and tested
  - ✅ Data models and validation working
  - ✅ Database integration functional
  - _Requirements: 1, 2, 5_

### Phase 2: Simple Stats ✅ COMPLETE

- [x] 4. Implement wrestler statistics
  - [x] 4.1 Calculate basic stats
    - ✅ Wins, losses, win percentage
    - ✅ Pin/Decision/Tech Fall/Major Decision counts
    - ✅ Simple match type breakdown
    - ✅ No complex metrics or predictions
    - _Requirements: 3_

  - [x] 4.2 Create analytics functions
    - ✅ `calculateWrestlerStats()` - core stats calculation
    - ✅ `getAllWrestlersWithStats()` - for wrestler list page
    - ✅ `getWrestlerMatches()` - for wrestler profile page
    - ✅ Unit tests with mocked Supabase calls
    - _Requirements: 3_

### Phase 3: Dashboard (MVP - 2 Pages Only)

- [x] 5. Set up simplified database schema
  - [x] 5.1 Update Supabase tables
    - Use simplified schema: wrestlers, tournaments, matches only
    - Remove teams, scraper_jobs, complex constraints
    - Essential indexes only
    - _Requirements: 2_

- [-] 6. Build Page 1: Wrestlers List
  - [x] 6.1 Create wrestlers list page
    - Table of wrestlers with basic stats
    - Columns: Name, Weight Class, Wins, Losses, Win %
    - Clickable rows to wrestler profiles
    - Simple search/filter by name
    - _Requirements: 4_

- [x] 7. Build Page 2: Wrestler Profile
  - [x] 7.1 Create wrestler profile page
    - Individual wrestler statistics display
    - Match history table (recent matches)
    - Simple stats: W-L record, match type breakdown
    - No fancy charts or complex analytics
    - _Requirements: 4_

### Phase 4: Deploy & Ship

- [x] 8. Deploy to production
  - [x] 8.1 Deploy dashboard to Vercel
    - Connect GitHub repository
    - Set up environment variables
    - Test production deployment
    - _Requirements: 4_

  - [x] 8.2 Document manual scraper usage
    - README with setup instructions
    - How to run scraper manually
    - Basic troubleshooting guide
    - _Requirements: 1_

## Removed from MVP (Post-Launch Features)

These were removed to keep MVP scope realistic:

❌ **Removed Tables**: teams, scraper_jobs (compute teams from wrestler data if needed later)
❌ **Removed Pages**: Home, Tournaments, Teams (focus on 2 core pages)
❌ **Removed Analytics**: Advanced metrics, predictions, trends, opponent strength
❌ **Removed Features**: Real-time updates, automation, notifications, complex UI
❌ **Removed Complexity**: Multiple weight class filters, tournament brackets, fancy charts

## Current Status Summary

### ✅ **COMPLETED (Ready to Use)**
- **Database**: Full Supabase schema with all tables and relationships
- **Python Scraper**: Complete scraping, validation, and database insertion
- **Data Pipeline**: End-to-end data flow from DubStat to Supabase
- **Dashboard Foundation**: Next.js project setup with Supabase integration
- **Analytics Engine**: Simple wrestler statistics (wins, losses, win %, match types)

### 🔄 **NEXT STEPS (True MVP)**
- **Simplified Database**: Update to 3 tables only (wrestlers, tournaments, matches)
- **2 Pages Only**: Wrestlers list + Wrestler profile pages
- **Deploy & Ship**: Get it working and deployed

### 📋 **IMMEDIATE NEXT TASKS**
1. **Update Database**: Simplify to MVP schema (3 tables)
2. **Build Wrestlers List**: Table with basic stats, clickable rows
3. **Build Wrestler Profile**: Individual stats and match history
4. **Deploy**: Ship to Vercel with manual scraper

## Success Criteria (MVP)

**Phase 1 Complete**: ✅ Can scrape tournament data and store in database
**Phase 2 Complete**: ✅ Can calculate basic wrestling statistics  
**Phase 3 Complete**: Working 2-page dashboard (wrestlers list + profile)
**Phase 4 Complete**: Deployed and documented

**MVP Success**: Answers "Can I see wrestling stats for my teammates?" - Nothing more.

The goal is a working wrestling analytics system that provides core value, built with simple, maintainable code that can be finished quickly.