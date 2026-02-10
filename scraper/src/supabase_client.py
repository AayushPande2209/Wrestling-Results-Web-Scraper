"""
Supabase client for wrestling analytics data operations.
"""
import os
import uuid
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import logging
from supabase import create_client, Client
import psycopg2
from psycopg2.extras import RealDictCursor

from .models import WrestlerData, MatchData, TournamentData, MatchType
from .data_validator import DataValidator


logger = logging.getLogger(__name__)


class SupabaseClientError(Exception):
    """Custom exception for Supabase client errors."""
    pass


class SupabaseClient:
    """Client for interacting with Supabase database."""
    
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize Supabase client.
        
        Args:
            url: Supabase project URL (defaults to SUPABASE_URL env var)
            key: Supabase key (defaults to SUPABASE_SERVICE_ROLE_KEY for writes, 
                falls back to SUPABASE_ANON_KEY)
        """
        self.url = url or os.getenv('SUPABASE_URL')
        # Prefer service_role key for write operations, fall back to anon key
        self.key = key or os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_ANON_KEY')
        
        if not self.url or not self.key:
            raise SupabaseClientError("Supabase URL and key are required")
        
        try:
            self.client: Client = create_client(self.url, self.key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise SupabaseClientError(f"Failed to initialize client: {e}")
        
        self.validator = DataValidator()
    
    def batch_insert_matches(self, matches: List[MatchData]) -> bool:
        """
        Insert multiple matches in batch with duplicate detection.
        
        Args:
            matches: List of MatchData objects to insert
            
        Returns:
            True if successful, False otherwise
        """
        if not matches:
            logger.warning("No matches to insert")
            return True
        
        try:
            logger.info(f"Starting batch insert of {len(matches)} matches")
            
            # Validate all matches first
            valid_matches = []
            skipped_invalid = 0
            for match in matches:
                if self.validator.validate_match_data(match):
                    valid_matches.append(self.validator.clean_match_data(match))
                else:
                    logger.warning(f"Skipping invalid match: {match}")
                    skipped_invalid += 1
            
            if not valid_matches:
                logger.warning("No valid matches to insert after validation")
                return False
            
            # Process matches in smaller batches to avoid timeouts
            batch_size = 50
            total_inserted = 0
            total_updated = 0
            total_skipped = 0
            
            for i in range(0, len(valid_matches), batch_size):
                batch = valid_matches[i:i + batch_size]
                inserted, updated, skipped = self._insert_match_batch(batch)
                total_inserted += inserted
                total_updated += updated
                total_skipped += skipped
                logger.info(f"Batch {i//batch_size + 1}: {inserted} inserted, {updated} updated, {skipped} skipped")
            
            logger.info(f"Summary: {total_inserted} inserted, {total_updated} updated, {total_skipped} skipped, {skipped_invalid} invalid (out of {len(matches)} total)")
            return (total_inserted + total_updated) > 0
            
        except Exception as e:
            logger.error(f"Failed to batch insert matches: {e}")
            return False
    
    def _insert_match_batch(self, matches: List[MatchData]) -> int:
        """Insert a single batch of matches, or update existing matches with 0-0 scores."""
        inserted_count = 0
        
        for match in matches:
            try:
                # Ensure wrestlers and tournament exist
                wrestler1_id = self._ensure_wrestler_exists(match.wrestler1)
                wrestler2_id = self._ensure_wrestler_exists(match.wrestler2)
                tournament_id = self._ensure_tournament_exists(match)
                
                # Check for existing match
                existing_match = self._find_existing_match(match, wrestler1_id, wrestler2_id, tournament_id)
                
                if existing_match:
                    # Match exists - check if we should update it
                    if existing_match['wrestler1_score'] == 0 and existing_match['wrestler2_score'] == 0:
                        # Update the match with new scores
                        if self._update_match_scores(
                            existing_match['id'],
                            match.wrestler1_score,
                            match.wrestler2_score,
                            match.match_type.value,
                            match.match_time
                        ):
                            logger.info(f"Updated match scores: {match.wrestler1.name} vs {match.wrestler2.name} ({match.tournament_name}, {match.round})")
                            inserted_count += 1
                        else:
                            logger.warning(f"Failed to update match: {match.wrestler1.name} vs {match.wrestler2.name}")
                    else:
                        # Match already has scores, skip it
                        logger.debug(f"Skipping match (already has scores): {match.wrestler1.name} vs {match.wrestler2.name} ({match.tournament_name}, {match.round})")
                    continue
                
                # Match doesn't exist - insert it
                match_data = {
                    'id': str(uuid.uuid4()),
                    'tournament_id': tournament_id,
                    'wrestler1_id': wrestler1_id,
                    'wrestler2_id': wrestler2_id,
                    'winner_id': self._get_winner_id(match, wrestler1_id, wrestler2_id),
                    'wrestler1_score': match.wrestler1_score,
                    'wrestler2_score': match.wrestler2_score,
                    'match_type': match.match_type.value,
                    'round': match.round,
                    'match_time': match.match_time,
                    'created_at': datetime.now().isoformat()
                }
                
                try:
                    result = self.client.table('matches').insert(match_data).execute()
                    if result.data:
                        inserted_count += 1
                        logger.debug(f"Inserted match: {match.wrestler1.name} vs {match.wrestler2.name}")
                except Exception as insert_err:
                    # Treat unique constraint violation (23505) as duplicate skip
                    if self._is_unique_violation(insert_err):
                        logger.info(f"Skipping duplicate match (DB constraint): {match.wrestler1.name} vs {match.wrestler2.name} ({match.tournament_name}, {match.round})")
                    else:
                        logger.error(f"Failed to insert match {match.wrestler1.name} vs {match.wrestler2.name}: {insert_err}")
                
            except Exception as e:
                logger.error(f"Failed to insert individual match: {e}")
                continue
        
        return inserted_count
    
    def _ensure_wrestler_exists(self, wrestler: WrestlerData) -> str:
        """Ensure wrestler exists in database and return ID - MVP simplified."""
        try:
            # First check if wrestler already exists
            result = self.client.table('wrestlers').select('id').eq('name', wrestler.name).execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Create new wrestler (no team reference in MVP)
            wrestler_data = {
                'id': str(uuid.uuid4()),
                'name': wrestler.name,
                'weight_class': wrestler.weight_class,
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('wrestlers').insert(wrestler_data).execute()
            if result.data:
                logger.debug(f"Created new wrestler: {wrestler.name}")
                return result.data[0]['id']
            else:
                raise SupabaseClientError(f"Failed to create wrestler: {wrestler.name}")
                
        except Exception as e:
            logger.error(f"Failed to ensure wrestler exists: {e}")
            raise
    
    # Removed _ensure_team_exists - not needed for MVP simplified schema
    
    def _ensure_tournament_exists(self, match: MatchData) -> str:
        """Ensure tournament exists in database and return ID - MVP simplified."""
        try:
            # Check if tournament already exists
            result = self.client.table('tournaments').select('id').eq('name', match.tournament_name).execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Create new tournament (simplified)
            tournament_data = {
                'id': str(uuid.uuid4()),
                'name': match.tournament_name,
                'date': match.date.date().isoformat() if match.date else None,
                'created_at': datetime.now().isoformat()
            }
            
            result = self.client.table('tournaments').insert(tournament_data).execute()
            if result.data:
                logger.debug(f"Created new tournament: {match.tournament_name}")
                return result.data[0]['id']
            else:
                raise SupabaseClientError(f"Failed to create tournament: {match.tournament_name}")
                
        except Exception as e:
            logger.error(f"Failed to ensure tournament exists: {e}")
            raise
    
    def _is_unique_violation(self, exc: Exception) -> bool:
        """Return True if the exception is a PostgreSQL unique constraint violation (23505)."""
        msg = str(exc).lower()
        if '23505' in msg or 'unique constraint' in msg or 'duplicate key' in msg:
            return True
        # Supabase/PostgREST may nest the error
        if hasattr(exc, 'message') and exc.message:
            return '23505' in str(exc.message) or 'unique' in str(exc.message).lower()
        return False

    def _is_duplicate_match(self, match: MatchData, wrestler1_id: str, wrestler2_id: str, tournament_id: str) -> bool:
        """Check if match already exists in database."""
        existing = self._find_existing_match(match, wrestler1_id, wrestler2_id, tournament_id)
        return existing is not None
    
    def _find_existing_match(self, match: MatchData, wrestler1_id: str, wrestler2_id: str, tournament_id: str) -> Optional[Dict[str, Any]]:
        """Find an existing match in the database. Returns the match data if found, None otherwise."""
        try:
            # Check for exact match (same wrestlers, tournament, round)
            result = self.client.table('matches').select('*').match({
                'tournament_id': tournament_id,
                'wrestler1_id': wrestler1_id,
                'wrestler2_id': wrestler2_id,
                'round': match.round
            }).execute()
            
            if result.data:
                return result.data[0]
            
            # Check for reverse match (wrestlers swapped)
            result = self.client.table('matches').select('*').match({
                'tournament_id': tournament_id,
                'wrestler1_id': wrestler2_id,
                'wrestler2_id': wrestler1_id,
                'round': match.round
            }).execute()
            
            if result.data:
                return result.data[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to find existing match: {e}")
            return None
    
    def _update_match_scores(self, match_id: str, wrestler1_score: int, wrestler2_score: int, 
                            match_type: str, match_time: Optional[str] = None) -> bool:
        """Update match scores and match type for an existing match."""
        try:
            update_data = {
                'wrestler1_score': wrestler1_score,
                'wrestler2_score': wrestler2_score,
                'match_type': match_type
            }
            
            # Only update match_time if it's provided
            if match_time:
                update_data['match_time'] = match_time
            
            result = self.client.table('matches').update(update_data).eq('id', match_id).execute()
            
            if result.data:
                logger.debug(f"Updated match {match_id} with scores {wrestler1_score}-{wrestler2_score}")
                return True
            else:
                logger.warning(f"No data returned when updating match {match_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update match scores for {match_id}: {e}")
            return False
    
    def _get_winner_id(self, match: MatchData, wrestler1_id: str, wrestler2_id: str) -> Optional[str]:
        """Get winner ID based on match data."""
        if not match.winner:
            return None
        
        if match.winner.name == match.wrestler1.name:
            return wrestler1_id
        elif match.winner.name == match.wrestler2.name:
            return wrestler2_id
        else:
            return None
    
    def update_wrestler_stats(self, wrestler_id: str) -> bool:
        """Update wrestler statistics based on match results - MVP simplified."""
        try:
            # Note: In MVP, we don't store wins/losses in wrestler table
            # Stats are computed on-demand from match data
            # This method is kept for compatibility but doesn't update stored stats
            logger.debug(f"Stats computation moved to analytics layer for wrestler: {wrestler_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update wrestler stats: {e}")
            return False
    
    def get_wrestler_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get wrestler data by name."""
        try:
            result = self.client.table('wrestlers').select('*').eq('name', name).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get wrestler by name: {e}")
            return None
    
    def get_tournament_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get tournament data by name."""
        try:
            result = self.client.table('tournaments').select('*').eq('name', name).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get tournament by name: {e}")
            return None
    
    def get_matches_for_tournament(self, tournament_id: str) -> List[Dict[str, Any]]:
        """Get all matches for a tournament."""
        try:
            result = self.client.table('matches').select('*').eq('tournament_id', tournament_id).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Failed to get matches for tournament: {e}")
            return []
    
    # Removed scraper job methods - not needed for MVP
    # Job tracking can be done through logs instead of database
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            result = self.client.table('wrestlers').select('id').limit(1).execute()
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False