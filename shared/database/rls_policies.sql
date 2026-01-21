-- Row Level Security (RLS) Policies for Wrestling Analytics Platform
-- These policies control data access and ensure proper security

-- Enable RLS on all tables
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE tournaments ENABLE ROW LEVEL SECURITY;
ALTER TABLE wrestlers ENABLE ROW LEVEL SECURITY;
ALTER TABLE matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE scraper_jobs ENABLE ROW LEVEL SECURITY;

-- Public read access for all data (wrestling data is generally public)
-- In production, you may want to restrict this based on authentication

-- Teams policies
CREATE POLICY "Public read access for teams" ON teams
    FOR SELECT USING (true);

CREATE POLICY "Authenticated insert for teams" ON teams
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Authenticated update for teams" ON teams
    FOR UPDATE USING (auth.role() = 'authenticated');

-- Tournaments policies
CREATE POLICY "Public read access for tournaments" ON tournaments
    FOR SELECT USING (true);

CREATE POLICY "Authenticated insert for tournaments" ON tournaments
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Authenticated update for tournaments" ON tournaments
    FOR UPDATE USING (auth.role() = 'authenticated');

-- Wrestlers policies
CREATE POLICY "Public read access for wrestlers" ON wrestlers
    FOR SELECT USING (true);

CREATE POLICY "Authenticated insert for wrestlers" ON wrestlers
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Authenticated update for wrestlers" ON wrestlers
    FOR UPDATE USING (auth.role() = 'authenticated');

-- Matches policies
CREATE POLICY "Public read access for matches" ON matches
    FOR SELECT USING (true);

CREATE POLICY "Authenticated insert for matches" ON matches
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Authenticated update for matches" ON matches
    FOR UPDATE USING (auth.role() = 'authenticated');

-- Scraper jobs policies (more restrictive - admin only)
CREATE POLICY "Authenticated read access for scraper_jobs" ON scraper_jobs
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Authenticated insert for scraper_jobs" ON scraper_jobs
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Authenticated update for scraper_jobs" ON scraper_jobs
    FOR UPDATE USING (auth.role() = 'authenticated');

-- Note: In a production environment, you would want to:
-- 1. Create specific roles for different access levels (admin, scraper, public)
-- 2. Implement more granular policies based on user roles
-- 3. Add policies for DELETE operations if needed
-- 4. Consider rate limiting and other security measures