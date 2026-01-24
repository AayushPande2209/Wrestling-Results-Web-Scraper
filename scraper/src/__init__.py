# Wrestling Analytics Scraper Package

from .models import WrestlerData, MatchData, TournamentData, MatchType, ScrapingJobStatus
from .playwright_scraper import PlaywrightScraper
from .data_validator import DataValidator, ValidationError

# Optional imports that require external dependencies
try:
    from .supabase_client import SupabaseClient, SupabaseClientError
    __all__ = [
        'WrestlerData',
        'MatchData', 
        'TournamentData',
        'MatchType',
        'ScrapingJobStatus',
        'PlaywrightScraper',
        'DataValidator',
        'ValidationError',
        'SupabaseClient',
        'SupabaseClientError'
    ]
except ImportError:
    # Supabase dependencies not available
    __all__ = [
        'WrestlerData',
        'MatchData', 
        'TournamentData',
        'MatchType',
        'ScrapingJobStatus',
        'PlaywrightScraper',
        'DataValidator',
        'ValidationError'
    ]