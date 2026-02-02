# Wrestling Analytics Database - MVP Setup

## Overview

This directory contains the simplified database schema for the Wrestling Analytics MVP. The MVP uses only 3 tables to keep things simple and focused on core functionality.

## MVP Schema (Simplified)

### Tables
- **wrestlers** - Individual wrestlers with basic info
- **tournaments** - Tournament information
- **matches** - Match results and scores

### Removed from Full Schema
- ❌ **teams** table - Teams computed from wrestler data if needed
- ❌ **scraper_jobs** table - Job tracking done through logs
- ❌ Complex constraints and triggers
- ❌ Updated_at columns and triggers
- ❌ Grade, division, location fields

## Files

### Schema Files
- `schema_mvp.sql` - Simplified 3-table schema (includes unique index to prevent duplicate matches)
- `setup_mvp.sql` - MVP setup script for Supabase
- `init_dev_data_mvp.sql` - Sample data for testing
- `unique_matches_constraint.sql` - Add unique index on matches for existing DBs (run after clearing matches if you deployed before this was in schema_mvp.sql)

### Legacy Files (Full Schema)
- `schema.sql` - Full schema with all tables
- `setup.sql` - Full setup script
- `init_dev_data.sql` - Full sample data
- `rls_policies.sql` - Row Level Security policies
- `realtime_config.sql` - Real-time configuration

## Setup Instructions

### 1. Supabase Setup (MVP)

1. Go to your Supabase project SQL editor
2. Run the MVP setup script:
   ```sql
   -- Copy and paste contents of setup_mvp.sql
   ```

### 2. Add Sample Data (Optional)

1. In Supabase SQL editor, run:
   ```sql
   -- Copy and paste contents of init_dev_data_mvp.sql
   ```

### 3. Verify Setup

Check that tables were created:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('wrestlers', 'tournaments', 'matches');
```

## MVP Schema Details

### wrestlers
```sql
CREATE TABLE wrestlers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    weight_class INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_weight_class CHECK (weight_class IN (106, 113, 120, 126, 132, 138, 145, 152, 160, 170, 182, 195, 220, 285))
);
```

### tournaments
```sql
CREATE TABLE tournaments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### matches
```sql
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tournament_id UUID REFERENCES tournaments(id) ON DELETE CASCADE,
    wrestler1_id UUID REFERENCES wrestlers(id) ON DELETE CASCADE,
    wrestler2_id UUID REFERENCES wrestlers(id) ON DELETE CASCADE,
    winner_id UUID REFERENCES wrestlers(id) ON DELETE SET NULL,
    wrestler1_score INTEGER DEFAULT 0,
    wrestler2_score INTEGER DEFAULT 0,
    match_type VARCHAR(50) DEFAULT 'decision',
    round VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Essential constraints only
    CONSTRAINT valid_match_type CHECK (match_type IN ('decision', 'major_decision', 'tech_fall', 'pin', 'forfeit', 'disqualification')),
    CONSTRAINT different_wrestlers CHECK (wrestler1_id != wrestler2_id),
    CONSTRAINT winner_is_participant CHECK (winner_id IS NULL OR winner_id = wrestler1_id OR winner_id = wrestler2_id),
    CONSTRAINT non_negative_scores CHECK (wrestler1_score >= 0 AND wrestler2_score >= 0)
);
```

## Key Simplifications

1. **No Teams Table**: Teams can be computed from wrestler data if needed later
2. **No Job Tracking**: Scraper jobs tracked in logs, not database
3. **Minimal Constraints**: Only essential business rules enforced
4. **No Triggers**: No automatic updated_at or complex logic
5. **Essential Indexes Only**: Just what's needed for basic queries

## Migration from Full Schema

If you have the full schema and want to migrate to MVP:

1. **Backup your data** first!
2. Export wrestler, tournament, and match data
3. Drop the full schema tables
4. Run the MVP setup
5. Import your data (may need transformation)

## Next Steps

After MVP setup:
1. Test with Python scraper
2. Verify dashboard connection
3. Add sample data for testing
4. Deploy and iterate

The MVP schema is designed to be simple and focused. Additional features can be added later as the system grows.