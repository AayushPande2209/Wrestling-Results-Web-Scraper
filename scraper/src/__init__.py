# Wrestling Analytics Scraper Package

from .models import WrestlerData, MatchData, TournamentData, MatchType, ScrapingJobStatus
from .dubstat_scraper import DubStatScraper
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
        'DubStatScraper',
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
        'DubStatScraper',
        'DataValidator',
        'ValidationError'
    ]