-- Wrestling Analytics Platform Database Schema
-- Supabase PostgreSQL Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Teams table
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    school VARCHAR(255),
    division VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tournaments table
CREATE TABLE tournaments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    date DATE,
    location VARCHAR(255),
    division VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Wrestlers table
CREATE TABLE wrestlers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    team_id UUID REFERENCES teams(id) ON DELETE SET NULL,
    weight_class INTEGER,
    grade INTEGER,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_weight_class CHECK (weight_class IN (106, 113, 120, 126, 132, 138, 145, 152, 160, 170, 182, 195, 220, 285)),
    CONSTRAINT valid_grade CHECK (grade >= 9 AND grade <= 12),
    CONSTRAINT non_negative_wins CHECK (wins >= 0),
    CONSTRAINT non_negative_losses CHECK (losses >= 0)
);

-- Scraper jobs table for tracking manual executions
CREATE TABLE scraper_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    status VARCHAR(50) NOT NULL DEFAULT 'running',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    tournament_urls TEXT[],
    matches_found INTEGER DEFAULT 0,
    matches_inserted INTEGER DEFAULT 0,
    error_message TEXT,
    triggered_by VARCHAR(100) DEFAULT 'manual',
    
    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('running', 'completed', 'failed')),
    CONSTRAINT valid_triggered_by CHECK (triggered_by IN ('manual', 'scheduled', 'api')),
    CONSTRAINT non_negative_matches_found CHECK (matches_found >= 0),
    CONSTRAINT non_negative_matches_inserted CHECK (matches_inserted >= 0)
);

-- Matches table
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
    match_time TIME,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_match_type CHECK (match_type IN ('decision', 'major_decision', 'tech_fall', 'pin', 'forfeit', 'disqualification')),
    CONSTRAINT different_wrestlers CHECK (wrestler1_id != wrestler2_id),
    CONSTRAINT winner_is_participant CHECK (winner_id IS NULL OR winner_id = wrestler1_id OR winner_id = wrestler2_id),
    CONSTRAINT non_negative_scores CHECK (wrestler1_score >= 0 AND wrestler2_score >= 0),
    CONSTRAINT reasonable_scores CHECK (wrestler1_score <= 50 AND wrestler2_score <= 50)
);

-- Indexes for performance
CREATE INDEX idx_wrestlers_team_id ON wrestlers(team_id);
CREATE INDEX idx_wrestlers_weight_class ON wrestlers(weight_class);
CREATE INDEX idx_wrestlers_name ON wrestlers(name);
CREATE INDEX idx_matches_tournament_id ON matches(tournament_id);
CREATE INDEX idx_matches_wrestler1_id ON matches(wrestler1_id);
CREATE INDEX idx_matches_wrestler2_id ON matches(wrestler2_id);
CREATE INDEX idx_matches_winner_id ON matches(winner_id);
CREATE INDEX idx_tournaments_date ON tournaments(date);
CREATE INDEX idx_scraper_jobs_status ON scraper_jobs(status);
CREATE INDEX idx_scraper_jobs_started_at ON scraper_jobs(started_at);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tournaments_updated_at BEFORE UPDATE ON tournaments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_wrestlers_updated_at BEFORE UPDATE ON wrestlers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();