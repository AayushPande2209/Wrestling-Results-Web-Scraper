-- Real-time subscriptions configuration for Wrestling Analytics Platform
-- Enables real-time updates for dashboard components

-- Enable real-time for all tables
ALTER PUBLICATION supabase_realtime ADD TABLE teams;
ALTER PUBLICATION supabase_realtime ADD TABLE tournaments;
ALTER PUBLICATION supabase_realtime ADD TABLE wrestlers;
ALTER PUBLICATION supabase_realtime ADD TABLE matches;
ALTER PUBLICATION supabase_realtime ADD TABLE scraper_jobs;

-- Function to update wrestler statistics when matches are inserted/updated
CREATE OR REPLACE FUNCTION update_wrestler_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Update wins/losses for wrestler1
    UPDATE wrestlers 
    SET wins = (
        SELECT COUNT(*) FROM matches 
        WHERE (wrestler1_id = NEW.wrestler1_id OR wrestler2_id = NEW.wrestler1_id) 
        AND winner_id = NEW.wrestler1_id
    ),
    losses = (
        SELECT COUNT(*) FROM matches 
        WHERE (wrestler1_id = NEW.wrestler1_id OR wrestler2_id = NEW.wrestler1_id) 
        AND winner_id != NEW.wrestler1_id AND winner_id IS NOT NULL
    )
    WHERE id = NEW.wrestler1_id;
    
    -- Update wins/losses for wrestler2
    UPDATE wrestlers 
    SET wins = (
        SELECT COUNT(*) FROM matches 
        WHERE (wrestler1_id = NEW.wrestler2_id OR wrestler2_id = NEW.wrestler2_id) 
        AND winner_id = NEW.wrestler2_id
    ),
    losses = (
        SELECT COUNT(*) FROM matches 
        WHERE (wrestler1_id = NEW.wrestler2_id OR wrestler2_id = NEW.wrestler2_id) 
        AND winner_id != NEW.wrestler2_id AND winner_id IS NOT NULL
    )
    WHERE id = NEW.wrestler2_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update wrestler statistics
CREATE TRIGGER update_wrestler_stats_trigger
    AFTER INSERT OR UPDATE ON matches
    FOR EACH ROW
    EXECUTE FUNCTION update_wrestler_stats();

-- Function to prevent duplicate matches
CREATE OR REPLACE FUNCTION prevent_duplicate_matches()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if a match with the same participants, tournament, and round already exists
    IF EXISTS (
        SELECT 1 FROM matches 
        WHERE tournament_id = NEW.tournament_id 
        AND round = NEW.round
        AND (
            (wrestler1_id = NEW.wrestler1_id AND wrestler2_id = NEW.wrestler2_id) OR
            (wrestler1_id = NEW.wrestler2_id AND wrestler2_id = NEW.wrestler1_id)
        )
        AND id != COALESCE(NEW.id, uuid_generate_v4())
    ) THEN
        RAISE EXCEPTION 'Duplicate match detected for tournament %, round %, wrestlers % and %', 
            NEW.tournament_id, NEW.round, NEW.wrestler1_id, NEW.wrestler2_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to prevent duplicate matches
CREATE TRIGGER prevent_duplicate_matches_trigger
    BEFORE INSERT OR UPDATE ON matches
    FOR EACH ROW
    EXECUTE FUNCTION prevent_duplicate_matches();

-- Function to validate match winner
CREATE OR REPLACE FUNCTION validate_match_winner()
RETURNS TRIGGER AS $$
BEGIN
    -- Ensure winner is one of the participants (if not null)
    IF NEW.winner_id IS NOT NULL AND 
       NEW.winner_id != NEW.wrestler1_id AND 
       NEW.winner_id != NEW.wrestler2_id THEN
        RAISE EXCEPTION 'Winner must be one of the match participants';
    END IF;
    
    -- For decision matches, ensure winner has higher score
    IF NEW.match_type = 'decision' AND NEW.winner_id IS NOT NULL THEN
        IF (NEW.winner_id = NEW.wrestler1_id AND NEW.wrestler1_score <= NEW.wrestler2_score) OR
           (NEW.winner_id = NEW.wrestler2_id AND NEW.wrestler2_score <= NEW.wrestler1_score) THEN
            RAISE EXCEPTION 'Winner must have higher score for decision matches';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to validate match winner
CREATE TRIGGER validate_match_winner_trigger
    BEFORE INSERT OR UPDATE ON matches
    FOR EACH ROW
    EXECUTE FUNCTION validate_match_winner();