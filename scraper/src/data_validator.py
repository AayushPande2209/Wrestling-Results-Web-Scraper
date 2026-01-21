"""
Data validation and cleaning for wrestling analytics scraper.
"""
import re
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import logging

from .models import WrestlerData, MatchData, TournamentData, MatchType


logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for data validation errors."""
    pass


class DataValidator:
    """Class for validating and cleaning wrestling data."""
    
    # Standard wrestling weight classes
    VALID_WEIGHT_CLASSES = [
        106, 113, 120, 126, 132, 138, 145, 152, 160, 170, 182, 195, 220, 285
    ]
    
    # Maximum reasonable scores for validation
    MAX_SCORE = 50
    MIN_SCORE = 0
    
    # Name validation patterns
    NAME_PATTERN = re.compile(r'^[A-Za-z\s\-\.\']{2,50}$')
    TEAM_PATTERN = re.compile(r'^[A-Za-z0-9\s\-\.&]{1,100}$')
    
    def __init__(self):
        """Initialize the data validator."""
        self.validation_errors = []
    
    def validate_wrestler_data(self, wrestler: WrestlerData) -> bool:
        """
        Validate wrestler data against business rules.
        
        Args:
            wrestler: WrestlerData object to validate
            
        Returns:
            True if valid, False otherwise
        """
        is_valid = True
        errors = []
        
        # Validate name
        if not self._validate_wrestler_name(wrestler.name):
            errors.append(f"Invalid wrestler name: '{wrestler.name}'")
            is_valid = False
        
        # Validate team
        if not self._validate_team_name(wrestler.team):
            errors.append(f"Invalid team name: '{wrestler.team}'")
            is_valid = False
        
        # Validate weight class if provided
        if wrestler.weight_class is not None:
            if not self._validate_weight_class(wrestler.weight_class):
                errors.append(f"Invalid weight class: {wrestler.weight_class}")
                is_valid = False
        
        # Validate grade if provided
        if wrestler.grade is not None:
            if not self._validate_grade(wrestler.grade):
                errors.append(f"Invalid grade: {wrestler.grade}")
                is_valid = False
        
        # Validate win/loss counts
        if wrestler.wins < 0 or wrestler.losses < 0:
            errors.append(f"Invalid win/loss record: {wrestler.wins}-{wrestler.losses}")
            is_valid = False
        
        # Validate percentages
        if not (0 <= wrestler.win_percentage <= 1):
            errors.append(f"Invalid win percentage: {wrestler.win_percentage}")
            is_valid = False
        
        if wrestler.avg_score < 0:
            errors.append(f"Invalid average score: {wrestler.avg_score}")
            is_valid = False
        
        if errors:
            self.validation_errors.extend(errors)
            logger.warning(f"Wrestler validation errors: {errors}")
        
        return is_valid
    
    def validate_match_data(self, match: MatchData) -> bool:
        """
        Validate match data against business rules.
        
        Args:
            match: MatchData object to validate
            
        Returns:
            True if valid, False otherwise
        """
        is_valid = True
        errors = []
        
        # Validate tournament name
        if not match.tournament_name or len(match.tournament_name.strip()) < 2:
            errors.append("Invalid tournament name")
            is_valid = False
        
        # Validate wrestlers
        if not self.validate_wrestler_data(match.wrestler1):
            errors.append("Invalid wrestler1 data")
            is_valid = False
        
        if not self.validate_wrestler_data(match.wrestler2):
            errors.append("Invalid wrestler2 data")
            is_valid = False
        
        # Validate scores
        if not self._validate_score(match.wrestler1_score):
            errors.append(f"Invalid wrestler1 score: {match.wrestler1_score}")
            is_valid = False
        
        if not self._validate_score(match.wrestler2_score):
            errors.append(f"Invalid wrestler2 score: {match.wrestler2_score}")
            is_valid = False
        
        # Validate winner logic
        if match.winner:
            if match.winner not in [match.wrestler1, match.wrestler2]:
                errors.append("Winner must be one of the two wrestlers")
                is_valid = False
            
            # For non-pin matches, winner should have higher score
            if match.match_type not in [MatchType.PIN, MatchType.FORFEIT, MatchType.DISQUALIFICATION]:
                if match.winner == match.wrestler1 and match.wrestler1_score <= match.wrestler2_score:
                    errors.append("Winner score inconsistency")
                    is_valid = False
                elif match.winner == match.wrestler2 and match.wrestler2_score <= match.wrestler1_score:
                    errors.append("Winner score inconsistency")
                    is_valid = False
        
        # Validate round
        if not match.round or len(match.round.strip()) < 1:
            errors.append("Invalid round information")
            is_valid = False
        
        # Validate date if provided
        if match.date and not self._validate_date(match.date):
            errors.append(f"Invalid match date: {match.date}")
            is_valid = False
        
        if errors:
            self.validation_errors.extend(errors)
            logger.warning(f"Match validation errors: {errors}")
        
        return is_valid
    
    def validate_tournament_data(self, tournament: TournamentData) -> bool:
        """
        Validate tournament data against business rules.
        
        Args:
            tournament: TournamentData object to validate
            
        Returns:
            True if valid, False otherwise
        """
        is_valid = True
        errors = []
        
        # Validate tournament name
        if not tournament.name or len(tournament.name.strip()) < 2:
            errors.append("Invalid tournament name")
            is_valid = False
        
        # Validate date if provided
        if tournament.date and not self._validate_date(tournament.date):
            errors.append(f"Invalid tournament date: {tournament.date}")
            is_valid = False
        
        # Validate matches
        for i, match in enumerate(tournament.matches):
            if not self.validate_match_data(match):
                errors.append(f"Invalid match data at index {i}")
                is_valid = False
        
        # Validate weight classes
        for weight_class in tournament.weight_classes:
            if not self._validate_weight_class(weight_class):
                errors.append(f"Invalid weight class: {weight_class}")
                is_valid = False
        
        if errors:
            self.validation_errors.extend(errors)
            logger.warning(f"Tournament validation errors: {errors}")
        
        return is_valid
    
    def clean_wrestler_data(self, wrestler: WrestlerData) -> WrestlerData:
        """
        Clean and normalize wrestler data.
        
        Args:
            wrestler: WrestlerData object to clean
            
        Returns:
            Cleaned WrestlerData object
        """
        cleaned_wrestler = WrestlerData(
            name=self._clean_wrestler_name(wrestler.name),
            team=self._clean_team_name(wrestler.team),
            weight_class=wrestler.weight_class,
            grade=wrestler.grade,
            wins=max(0, wrestler.wins),
            losses=max(0, wrestler.losses),
            win_percentage=max(0, min(1, wrestler.win_percentage)),
            avg_score=max(0, wrestler.avg_score),
            recent_form=wrestler.recent_form.copy()
        )
        
        return cleaned_wrestler
    
    def clean_match_data(self, match: MatchData) -> MatchData:
        """
        Clean and normalize match data.
        
        Args:
            match: MatchData object to clean
            
        Returns:
            Cleaned MatchData object
        """
        cleaned_match = MatchData(
            tournament_name=self._clean_tournament_name(match.tournament_name),
            wrestler1=self.clean_wrestler_data(match.wrestler1),
            wrestler2=self.clean_wrestler_data(match.wrestler2),
            winner=self.clean_wrestler_data(match.winner) if match.winner else None,
            wrestler1_score=max(0, min(self.MAX_SCORE, match.wrestler1_score)),
            wrestler2_score=max(0, min(self.MAX_SCORE, match.wrestler2_score)),
            match_type=match.match_type,
            round=self._clean_round_info(match.round),
            match_time=match.match_time,
            date=match.date
        )
        
        return cleaned_match
    
    def clean_tournament_data(self, tournament: TournamentData) -> TournamentData:
        """
        Clean and normalize tournament data.
        
        Args:
            tournament: TournamentData object to clean
            
        Returns:
            Cleaned TournamentData object
        """
        cleaned_tournament = TournamentData(
            name=self._clean_tournament_name(tournament.name),
            date=tournament.date,
            location=self._clean_location(tournament.location) if tournament.location else None,
            division=self._clean_division(tournament.division) if tournament.division else None,
            matches=[self.clean_match_data(match) for match in tournament.matches],
            participating_teams=[self._clean_team_name(team) for team in tournament.participating_teams],
            weight_classes=[wc for wc in tournament.weight_classes if self._validate_weight_class(wc)]
        )
        
        return cleaned_tournament
    
    def _validate_wrestler_name(self, name: str) -> bool:
        """Validate wrestler name format."""
        if not name or not isinstance(name, str):
            return False
        return bool(self.NAME_PATTERN.match(name.strip()))
    
    def _validate_team_name(self, team: str) -> bool:
        """Validate team name format."""
        if not team or not isinstance(team, str):
            return False
        return bool(self.TEAM_PATTERN.match(team.strip()))
    
    def _validate_weight_class(self, weight_class: int) -> bool:
        """Validate weight class against standard wrestling weights."""
        return weight_class in self.VALID_WEIGHT_CLASSES
    
    def _validate_grade(self, grade: int) -> bool:
        """Validate grade level (9-12 for high school)."""
        return 9 <= grade <= 12
    
    def _validate_score(self, score: int) -> bool:
        """Validate match score."""
        return self.MIN_SCORE <= score <= self.MAX_SCORE
    
    def _validate_date(self, date: datetime) -> bool:
        """Validate date is reasonable (within last 5 years to next year)."""
        current_year = datetime.now().year
        return (current_year - 5) <= date.year <= (current_year + 1)
    
    def _clean_wrestler_name(self, name: str) -> str:
        """Clean and standardize wrestler name."""
        if not name:
            return "Unknown"
        
        # Remove extra whitespace and normalize
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        # Handle common name patterns
        name = re.sub(r'\b([A-Z])\.', r'\1.', name)  # Fix initials
        name = re.sub(r'\s+', ' ', name)  # Remove multiple spaces
        
        return name.strip()
    
    def _clean_team_name(self, team: str) -> str:
        """Clean and standardize team name."""
        if not team:
            return "Unknown"
        
        # Remove extra whitespace and normalize
        team = ' '.join(team.split())
        
        # Capitalize properly
        team = team.title()
        
        # Handle common abbreviations
        team = re.sub(r'\bHs\b', 'HS', team)  # High School
        team = re.sub(r'\bMs\b', 'MS', team)  # Middle School
        
        return team.strip()
    
    def _clean_tournament_name(self, name: str) -> str:
        """Clean and standardize tournament name."""
        if not name:
            return "Unknown Tournament"
        
        # Remove extra whitespace and normalize
        name = ' '.join(name.split())
        
        # Capitalize properly
        name = name.title()
        
        return name.strip()
    
    def _clean_round_info(self, round_info: str) -> str:
        """Clean and standardize round information."""
        if not round_info:
            return "Unknown Round"
        
        # Remove extra whitespace and normalize
        round_info = ' '.join(round_info.split())
        
        # Capitalize properly
        round_info = round_info.title()
        
        # Standardize common round names
        round_mapping = {
            'Quarters': 'Quarterfinals',
            'Semis': 'Semifinals',
            'Finals': 'Championship',
            'Champ': 'Championship',
            'Cons': 'Consolation'
        }
        
        for abbrev, full_name in round_mapping.items():
            if abbrev.lower() in round_info.lower():
                round_info = full_name
                break
        
        return round_info.strip()
    
    def _clean_location(self, location: str) -> str:
        """Clean and standardize location information."""
        if not location:
            return None
        
        # Remove extra whitespace and normalize
        location = ' '.join(location.split())
        
        # Capitalize properly
        location = location.title()
        
        return location.strip()
    
    def _clean_division(self, division: str) -> str:
        """Clean and standardize division information."""
        if not division:
            return None
        
        # Remove extra whitespace and normalize
        division = ' '.join(division.split())
        
        # Standardize common divisions
        division_mapping = {
            'varsity': 'Varsity',
            'jv': 'JV',
            'junior varsity': 'JV',
            'freshman': 'Freshman',
            'sophomore': 'Sophomore'
        }
        
        division_lower = division.lower()
        for key, value in division_mapping.items():
            if key in division_lower:
                division = value
                break
        
        return division.strip()
    
    def get_validation_errors(self) -> List[str]:
        """Get all validation errors collected during validation."""
        return self.validation_errors.copy()
    
    def clear_validation_errors(self) -> None:
        """Clear all collected validation errors."""
        self.validation_errors.clear()
    
    def has_validation_errors(self) -> bool:
        """Check if there are any validation errors."""
        return len(self.validation_errors) > 0