-- Wrestling Analytics Platform Database Setup Script
-- Run this script in your Supabase SQL editor to set up the complete database

-- Step 1: Create the schema
\i schema.sql

-- Step 2: Set up Row Level Security policies
\i rls_policies.sql

-- Step 3: Configure real-time subscriptions and triggers
\i realtime_config.sql

-- Step 4: Insert sample data for testing (optional)
-- Uncomment the following lines if you want sample data

/*
-- Sample teams
INSERT INTO teams (name, school, division) VALUES
('Eagles', 'Lincoln High School', 'Division I'),
('Tigers', 'Roosevelt High School', 'Division I'),
('Bears', 'Washington High School', 'Division II');

-- Sample tournament
INSERT INTO tournaments (name, date, location, division) VALUES
('State Championship', '2024-02-15', 'State Arena', 'Division I');

-- Sample wrestlers
INSERT INTO wrestlers (name, team_id, weight_class, grade, wins, losses) VALUES
('John Smith', (SELECT id FROM teams WHERE name = 'Eagles'), 152, 11, 15, 3),
('Mike Johnson', (SELECT id FROM teams WHERE name = 'Tigers'), 152, 12, 12, 5),
('Dave Wilson', (SELECT id FROM teams WHERE name = 'Bears'), 160, 10, 18, 2);

-- Sample match
INSERT INTO matches (
    tournament_id, 
    wrestler1_id, 
    wrestler2_id, 
    winner_id, 
    wrestler1_score, 
    wrestler2_score, 
    match_type, 
    round
) VALUES (
    (SELECT id FROM tournaments WHERE name = 'State Championship'),
    (SELECT id FROM wrestlers WHERE name = 'John Smith'),
    (SELECT id FROM wrestlers WHERE name = 'Mike Johnson'),
    (SELECT id FROM wrestlers WHERE name = 'John Smith'),
    7, 4, 'decision', 'Quarterfinals'
);
*/

-- Verification queries
SELECT 'Database setup completed successfully!' as status;
SELECT 'Tables created:' as info, count(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('teams', 'tournaments', 'wrestlers', 'matches', 'scraper_jobs');