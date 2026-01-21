-- Development Data Initialization
-- Sample data for testing and development

-- Clear existing data (be careful in production!)
TRUNCATE TABLE matches CASCADE;
TRUNCATE TABLE wrestlers CASCADE;
TRUNCATE TABLE tournaments CASCADE;
TRUNCATE TABLE teams CASCADE;
TRUNCATE TABLE scraper_jobs CASCADE;

-- Insert sample teams
INSERT INTO teams (id, name, school, division) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Eagles', 'Lincoln High School', 'Division I'),
('550e8400-e29b-41d4-a716-446655440002', 'Tigers', 'Roosevelt High School', 'Division I'),
('550e8400-e29b-41d4-a716-446655440003', 'Bears', 'Washington High School', 'Division II'),
('550e8400-e29b-41d4-a716-446655440004', 'Lions', 'Jefferson High School', 'Division I'),
('550e8400-e29b-41d4-a716-446655440005', 'Hawks', 'Madison High School', 'Division II');

-- Insert sample tournaments
INSERT INTO tournaments (id, name, date, location, division) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'State Championship', '2024-02-15', 'State Arena', 'Division I'),
('660e8400-e29b-41d4-a716-446655440002', 'Regional Tournament', '2024-01-20', 'Regional Center', 'Division I'),
('660e8400-e29b-41d4-a716-446655440003', 'District Meet', '2024-01-10', 'District Gym', 'Division II');

-- Insert sample wrestlers
INSERT INTO wrestlers (id, name, team_id, weight_class, grade, wins, losses) VALUES
-- Eagles team
('770e8400-e29b-41d4-a716-446655440001', 'John Smith', '550e8400-e29b-41d4-a716-446655440001', 152, 11, 15, 3),
('770e8400-e29b-41d4-a716-446655440002', 'Alex Johnson', '550e8400-e29b-41d4-a716-446655440001', 160, 12, 12, 6),
('770e8400-e29b-41d4-a716-446655440003', 'Chris Davis', '550e8400-e29b-41d4-a716-446655440001', 170, 10, 18, 2),

-- Tigers team
('770e8400-e29b-41d4-a716-446655440004', 'Mike Wilson', '550e8400-e29b-41d4-a716-446655440002', 152, 12, 14, 4),
('770e8400-e29b-41d4-a716-446655440005', 'Tom Brown', '550e8400-e29b-41d4-a716-446655440002', 160, 11, 16, 3),
('770e8400-e29b-41d4-a716-446655440006', 'Steve Miller', '550e8400-e29b-41d4-a716-446655440002', 170, 12, 13, 5),

-- Bears team
('770e8400-e29b-41d4-a716-446655440007', 'Dave Garcia', '550e8400-e29b-41d4-a716-446655440003', 152, 10, 17, 2),
('770e8400-e29b-41d4-a716-446655440008', 'Paul Martinez', '550e8400-e29b-41d4-a716-446655440003', 160, 11, 15, 4),
('770e8400-e29b-41d4-a716-446655440009', 'Ryan Lopez', '550e8400-e29b-41d4-a716-446655440003', 170, 12, 11, 7);

-- Insert sample matches
INSERT INTO matches (tournament_id, wrestler1_id, wrestler2_id, winner_id, wrestler1_score, wrestler2_score, match_type, round) VALUES
-- State Championship matches
('660e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440004', '770e8400-e29b-41d4-a716-446655440001', 7, 4, 'decision', 'Quarterfinals'),
('660e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440005', '770e8400-e29b-41d4-a716-446655440005', 3, 8, 'decision', 'Quarterfinals'),
('660e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440006', '770e8400-e29b-41d4-a716-446655440003', 0, 0, 'pin', 'Semifinals'),

-- Regional Tournament matches
('660e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440007', '770e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440007', 12, 5, 'major_decision', 'Finals'),
('660e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440008', '770e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440008', 6, 9, 'decision', 'Semifinals');

-- Insert sample scraper job
INSERT INTO scraper_jobs (id, status, started_at, completed_at, tournament_urls, matches_found, matches_inserted, triggered_by) VALUES
('880e8400-e29b-41d4-a716-446655440001', 'completed', NOW() - INTERVAL '1 hour', NOW() - INTERVAL '30 minutes', 
 ARRAY['https://dubstat.com/tournament1', 'https://dubstat.com/tournament2'], 25, 23, 'manual');

-- Verify data insertion
SELECT 'Development data initialized successfully!' as status;
SELECT 'Teams:' as table_name, count(*) as record_count FROM teams
UNION ALL
SELECT 'Tournaments:', count(*) FROM tournaments
UNION ALL
SELECT 'Wrestlers:', count(*) FROM wrestlers
UNION ALL
SELECT 'Matches:', count(*) FROM matches
UNION ALL
SELECT 'Scraper Jobs:', count(*) FROM scraper_jobs;