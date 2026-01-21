-- Wrestling Analytics Platform Database Schema - MVP Version
-- Simplified: Only wrestlers, tournaments, matches

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Wrestlers table - simplified
CREATE TABLE wrestlers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    weight_class INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Simple constraints
    CONSTRAINT valid_weight_class CHECK (weight_class IN (106, 113, 120, 126, 132, 138, 145, 152, 160, 170, 182, 195, 220, 285))
);

-- Tournaments table - minimal
CREATE TABLE tournaments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Matches table - core data only
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

-- Essential indexes only
CREATE INDEX idx_wrestlers_name ON wrestlers(name);
CREATE INDEX idx_wrestlers_weight_class ON wrestlers(weight_class);
CREATE INDEX idx_matches_wrestler1_id ON matches(wrestler1_id);
CREATE INDEX idx_matches_wrestler2_id ON matches(wrestler2_id);
CREATE INDEX idx_matches_tournament_id ON matches(tournament_id);
CREATE INDEX idx_tournaments_date ON tournaments(date);

-- Note: No teams table, no scraper_jobs table, no complex triggers
-- Teams can be computed from wrestler data if needed later
-- Scraper jobs can be tracked in logs, not database
-- Keep it simple for MVP!