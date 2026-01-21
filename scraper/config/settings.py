"""
Configuration settings for the Wrestling Analytics Scraper.
Loads environment variables and provides configuration management.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Configuration settings for the scraper application."""
    
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Scraper Configuration
    SCRAPER_USER_AGENT: str = os.getenv("SCRAPER_USER_AGENT", "Mozilla/5.0 (compatible; WrestlingAnalytics/1.0)")
    SCRAPER_REQUEST_TIMEOUT: int = int(os.getenv("SCRAPER_REQUEST_TIMEOUT", "30"))
    SCRAPER_MAX_RETRIES: int = int(os.getenv("SCRAPER_MAX_RETRIES", "3"))
    SCRAPER_RETRY_DELAY: int = int(os.getenv("SCRAPER_RETRY_DELAY", "1"))
    SCRAPER_BATCH_SIZE: int = int(os.getenv("SCRAPER_BATCH_SIZE", "100"))
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_RATE_LIMIT_PER_MINUTE: int = int(os.getenv("API_RATE_LIMIT_PER_MINUTE", "60"))
    
    # Environment Configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "./logs/wrestling_analytics.log")
    VERBOSE_LOGGING: bool = os.getenv("VERBOSE_LOGGING", "false").lower() == "true"
    
    @classmethod
    def validate_required_settings(cls) -> List[str]:
        """Validate that all required environment variables are set."""
        missing_settings = []
        
        required_settings = [
            ("SUPABASE_URL", cls.SUPABASE_URL),
            ("SUPABASE_ANON_KEY", cls.SUPABASE_ANON_KEY),
            ("SUPABASE_SERVICE_ROLE_KEY", cls.SUPABASE_SERVICE_ROLE_KEY),
        ]
        
        for setting_name, setting_value in required_settings:
            if not setting_value:
                missing_settings.append(setting_name)
        
        return missing_settings
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == "development"
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == "production"

# Global settings instance
settings = Settings()