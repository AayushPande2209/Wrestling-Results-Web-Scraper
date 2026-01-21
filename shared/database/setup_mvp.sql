-- Wrestling Analytics Platform Database Setup Script - MVP Version
-- Run this script in your Supabase SQL editor to set up the simplified database

-- Step 1: Create the simplified MVP schema
\i schema_mvp.sql

-- Step 2: Set up basic Row Level Security policies (optional for MVP)
-- \i rls_policies.sql

-- Step 3: Insert sample data for testing (optional)
-- Uncomment the following lines if you want sample data

/*
-- Sample tournaments
INSERT INTO tournaments (name, date) VALUES
('State Championship', '2024-02-15'),
('Regional Tournament', '2024-01-20'),
('District Meet', '2024-01-10');

-- Sample wrestlers (no teams - simplified)
INSERT INTO wrestlers (name, weight_class) VALUES
('John Smith', 152),
('Mike Johnson', 152),
('Dave Wilson', 160),
('Alex Brown', 160),
('Chris Davis', 170),
('Tom Miller', 170);

-- Sample matches
INSERT INTO matches (
    tournament_id, 
    wrestler1_id, 
    wrestler2_id, 
    winner_id, 
    wrestler1_score, 
    wrestler2_score, 
    match_type, 
    round
) VALUES 
(
    (SELECT id FROM tournaments WHERE name = 'State Championship'),
    (SELECT id FROM wrestlers WHERE name = 'John Smith'),
    (SELECT id FROM wrestlers WHERE name = 'Mike Johnson'),
    (SELECT id FROM wrestlers WHERE name = 'John Smith'),
    7, 4, 'decision', 'Quarterfinals'
),
(
    (SELECT id FROM tournaments WHERE name = 'State Championship'),
    (SELECT id FROM wrestlers WHERE name = 'Dave Wilson'),
    (SELECT id FROM wrestlers WHERE name = 'Alex Brown'),
    (SELECT id FROM wrestlers WHERE name = 'Dave Wilson'),
    0, 0, 'pin', 'Semifinals'
);
*/

-- Verification queries
SELECT 'MVP Database setup completed successfully!' as status;
SELECT 'Tables created:' as info, count(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('tournaments', 'wrestlers', 'matches');

-- Show table structure
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name IN ('wrestlers', 'tournaments', 'matches')
ORDER BY table_name, ordinal_position;