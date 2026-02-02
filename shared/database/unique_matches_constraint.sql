-- Prevent duplicate matches: same tournament, round, and wrestler pair (order-independent).
-- When to run:
-- - Existing DB: After you delete all matches, run this in the Supabase SQL editor.
-- - Fresh install: schema_mvp.sql already includes this index; no need to run separately.

-- Unique index: (tournament_id, round, canonical wrestler pair).
-- LEAST/GREATEST ensures "A vs B" and "B vs A" are treated as the same match.
CREATE UNIQUE INDEX IF NOT EXISTS idx_matches_unique_match
ON matches (
    tournament_id,
    COALESCE(round, ''),
    LEAST(wrestler1_id, wrestler2_id),
    GREATEST(wrestler1_id, wrestler2_id)
);
