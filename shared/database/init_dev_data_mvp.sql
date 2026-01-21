-- Development Data Initialization - MVP Version
-- Sample data for testing and development (simplified schema)

-- Clear existing data (be careful in production!)
TRUNCATE TABLE matches CASCADE;
TRUNCATE TABLE wrestlers CASCADE;
TRUNCATE TABLE tournaments CASCADE;

-- Insert sample tournaments
INSERT INTO tournaments (id, name, date) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'State Championship', '2024-02-15'),
('660e8400-e29b-41d4-a716-446655440002', 'Regional Tournament', '2024-01-20'),
('660e8400-e29b-41d4-a716-446655440003', 'District Meet', '2024-01-10');

-- Insert sample wrestlers (no teams - simplified)
INSERT INTO wrestlers (id, name, weight_class) VALUES
-- 152 weight class
('770e8400-e29b-41d4-a716-446655440001', 'John Smith', 152),
('770e8400-e29b-41d4-a716-446655440004', 'Mike Wilson', 152),
('770e8400-e29b-41d4-a716-446655440007', 'Dave Garcia', 152),

-- 160 weight class
('770e8400-e29b-41d4-a716-446655440002', 'Alex Johnson', 160),
('770e8400-e29b-41d4-a716-446655440005', 'Tom Brown', 160),
('770e8400-e29b-41d4-a716-446655440008', 'Paul Martinez', 160),

-- 170 weight class
('770e8400-e29b-41d4-a716-446655440003', 'Chris Davis', 170),
('770e8400-e29b-41d4-a716-446655440006', 'Steve Miller', 170),
('770e8400-e29b-41d4-a716-446655440009', 'Ryan Lopez', 170);

-- Insert sample matches
INSERT INTO matches (tournament_id, wrestler1_id, wrestler2_id, winner_id, wrestler1_score, wrestler2_score, match_type, round) VALUES
-- State Championship matches
('660e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440004', '770e8400-e29b-41d4-a716-446655440001', 7, 4, 'decision', 'Quarterfinals'),
('660e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440005', '770e8400-e29b-41d4-a716-446655440005', 3, 8, 'decision', 'Quarterfinals'),
('660e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440006', '770e8400-e29b-41d4-a716-446655440003', 0, 0, 'pin', 'Semifinals'),

-- Regional Tournament matches
('660e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440007', '770e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440007', 12, 5, 'major_decision', 'Finals'),
('660e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440008', '770e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440008', 6, 9, 'decision', 'Semifinals'),

-- District Meet matches
('660e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440009', '770e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440009', 15, 0, 'tech_fall', 'Finals'),
('660e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440004', '770e8400-e29b-41d4-a716-446655440007', '770e8400-e29b-41d4-a716-446655440004', 0, 0, 'pin', 'Semifinals');

-- Verify data insertion
SELECT 'MVP Development data initialized successfully!' as status;
SELECT 'Tournaments:' as table_name, count(*) as record_count FROM tournaments
UNION ALL
SELECT 'Wrestlers:', count(*) FROM wrestlers
UNION ALL
SELECT 'Matches:', count(*) FROM matches;

-- Show sample data
SELECT 'Sample wrestlers by weight class:' as info;
SELECT weight_class, count(*) as wrestler_count 
FROM wrestlers 
GROUP BY weight_class 
ORDER BY weight_class;

SELECT 'Sample matches by tournament:' as info;
SELECT t.name as tournament, count(m.id) as match_count
FROM tournaments t
LEFT JOIN matches m ON t.id = m.tournament_id
GROUP BY t.name
ORDER BY t.name;