"""
Data models for the wrestling analytics scraper.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class MatchType(Enum):
    """Wrestling match outcome types."""
    DECISION = "decision"
    MAJOR_DECISION = "major_decision"
    TECH_FALL = "tech_fall"
    PIN = "pin"
    FORFEIT = "forfeit"
    DISQUALIFICATION = "disqualification"


@dataclass
class WrestlerData:
    """Data model for wrestler information - MVP simplified."""
    name: str
    weight_class: Optional[int] = None
    # Removed: team, grade, wins, losses, win_percentage, avg_score, recent_form
    # These will be computed from match data when needed


@dataclass
class MatchData:
    """Data model for wrestling match information."""
    tournament_name: str
    wrestler1: WrestlerData
    wrestler2: WrestlerData
    winner: Optional[WrestlerData]
    wrestler1_score: int
    wrestler2_score: int
    match_type: MatchType
    round: str
    match_time: Optional[str] = None
    date: Optional[datetime] = None


@dataclass
class TournamentData:
    """Data model for tournament information - MVP simplified."""
    name: str
    date: Optional[datetime]
    matches: List[MatchData] = field(default_factory=list)
    # Removed: location, division, participating_teams, weight_classes
    # Keep it simple for MVP


# Removed ScrapingJobStatus - not needed for MVP
# Job tracking can be done through logs instead of database