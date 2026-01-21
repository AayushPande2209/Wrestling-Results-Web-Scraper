"""
DubStat scraper for extracting wrestling match data.
"""
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging
from urllib.parse import urljoin, urlparse

from .models import WrestlerData, MatchData, TournamentData, MatchType


logger = logging.getLogger(__name__)


class DubStatScraper:
    """Main scraper class for extracting wrestling data from DubStat pages."""
    
    def __init__(self, base_url: str = "https://www.dubstat.com"):
        """Initialize the scraper with base URL and session."""
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_tournament_page(self, url: str) -> List[MatchData]:
        """
        Scrape a tournament page and extract all match data.
        
        Args:
            url: URL of the tournament page to scrape
            
        Returns:
            List of MatchData objects extracted from the page
            
        Raises:
            requests.RequestException: If HTTP request fails
            ValueError: If page structure is unexpected
        """
        try:
            logger.info(f"Scraping tournament page: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            tournament_info = self._extract_tournament_info(soup, url)
            matches = self._extract_matches_from_page(soup, tournament_info)
            
            logger.info(f"Extracted {len(matches)} matches from {url}")
            return matches
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to parse {url}: {e}")
            raise ValueError(f"Could not parse tournament page: {e}")
    
    def _extract_tournament_info(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract tournament metadata from the page."""
        tournament_info = {
            'name': 'Unknown Tournament',
            'date': None,
            'location': None,
            'division': None
        }
        
        # Try to extract tournament name from title or header
        title_elem = soup.find('title')
        if title_elem:
            tournament_info['name'] = title_elem.get_text().strip()
        
        # Look for tournament name in common header patterns
        for selector in ['h1', '.tournament-title', '.event-title', '.page-title']:
            header = soup.select_one(selector)
            if header:
                tournament_info['name'] = header.get_text().strip()
                break
        
        # Try to extract date information
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\w+ \d{1,2}, \d{4})',
            r'(\d{4}-\d{2}-\d{2})'
        ]
        
        page_text = soup.get_text()
        for pattern in date_patterns:
            match = re.search(pattern, page_text)
            if match:
                try:
                    date_str = match.group(1)
                    # Try different date formats
                    for fmt in ['%m/%d/%Y', '%m-%d-%Y', '%B %d, %Y', '%Y-%m-%d']:
                        try:
                            tournament_info['date'] = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                    if tournament_info['date']:
                        break
                except Exception:
                    continue
        
        return tournament_info
    
    def _extract_matches_from_page(self, soup: BeautifulSoup, tournament_info: Dict[str, Any]) -> List[MatchData]:
        """Extract all matches from the tournament page."""
        matches = []
        
        # Common selectors for match data on wrestling sites
        match_selectors = [
            '.match-row',
            '.bout-row', 
            '.match-result',
            'tr.match',
            '.wrestling-match',
            'tbody tr'  # Generic table rows
        ]
        
        match_elements = []
        for selector in match_selectors:
            elements = soup.select(selector)
            if elements:
                match_elements = elements
                logger.debug(f"Found {len(elements)} potential matches using selector: {selector}")
                break
        
        if not match_elements:
            # Fallback: look for any table rows that might contain match data
            match_elements = soup.find_all('tr')
            logger.debug(f"Fallback: found {len(match_elements)} table rows")
        
        for element in match_elements:
            try:
                match_data = self._extract_match_from_element(element, tournament_info)
                if match_data:
                    matches.append(match_data)
            except Exception as e:
                logger.warning(f"Failed to extract match from element: {e}")
                continue
        
        return matches
    
    def _extract_match_from_element(self, element, tournament_info: Dict[str, Any]) -> Optional[MatchData]:
        """Extract match data from a single HTML element."""
        try:
            # Get all text content from the element
            text_content = element.get_text(separator=' ', strip=True)
            
            # Skip elements that don't look like match data
            if not self._looks_like_match_data(text_content):
                return None
            
            # Extract wrestler information
            wrestler_info = self._extract_wrestler_info(element)
            if len(wrestler_info) < 2:
                return None
            
            wrestler1, wrestler2 = wrestler_info[0], wrestler_info[1]
            
            # Extract scores
            scores = self._extract_scores(element)
            if not scores or len(scores) < 2:
                return None
            
            wrestler1_score, wrestler2_score = scores[0], scores[1]
            
            # Determine winner
            winner = wrestler1 if wrestler1_score > wrestler2_score else wrestler2
            
            # Extract match type and round
            match_type = self._extract_match_type(element)
            round_info = self._extract_round_info(element)
            
            return MatchData(
                tournament_name=tournament_info['name'],
                wrestler1=wrestler1,
                wrestler2=wrestler2,
                winner=winner,
                wrestler1_score=wrestler1_score,
                wrestler2_score=wrestler2_score,
                match_type=match_type,
                round=round_info,
                date=tournament_info['date']
            )
            
        except Exception as e:
            logger.debug(f"Could not extract match from element: {e}")
            return None
    
    def _looks_like_match_data(self, text: str) -> bool:
        """Check if text content looks like it contains match data."""
        # Look for patterns that suggest match data
        patterns = [
            r'\d+\s*-\s*\d+',  # Score pattern like "15-3"
            r'\b(pin|dec|md|tf|ff|dq)\b',  # Match type abbreviations
            r'\b\d{3}\b',  # Weight class like "152"
            r'vs\.?\s+',  # "vs" indicating opponents
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in patterns)
    
    def extract_wrestler_info(self, html_element) -> WrestlerData:
        """
        Extract wrestler information from an HTML element.
        
        Args:
            html_element: BeautifulSoup element containing wrestler data
            
        Returns:
            WrestlerData object with extracted information
        """
        # This method is called by the interface but delegates to internal method
        wrestler_info = self._extract_wrestler_info(html_element)
        return wrestler_info[0] if wrestler_info else WrestlerData("Unknown", "Unknown")
    
    def _extract_wrestler_info(self, element) -> List[WrestlerData]:
        """Extract wrestler information from match element."""
        wrestlers = []
        
        # Look for wrestler names in various patterns
        name_patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+)',  # First Last
            r'([A-Z]\. [A-Z][a-z]+)',      # F. Last
            r'([A-Z][a-z]+, [A-Z]\.)',     # Last, F.
        ]
        
        text = element.get_text()
        
        # Try to find team information
        team_patterns = [
            r'\(([^)]+)\)',  # Team in parentheses
            r'- ([A-Z]{2,4})',  # Team abbreviation after dash
        ]
        
        teams = []
        for pattern in team_patterns:
            matches = re.findall(pattern, text)
            teams.extend(matches)
        
        # Extract names
        names = []
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            names.extend(matches)
        
        # Create wrestler objects
        for i, name in enumerate(names[:2]):  # Limit to 2 wrestlers per match
            team = teams[i] if i < len(teams) else "Unknown"
            wrestlers.append(WrestlerData(name=name.strip(), team=team.strip()))
        
        return wrestlers
    
    def _extract_scores(self, element) -> List[int]:
        """Extract match scores from element."""
        text = element.get_text()
        
        # Look for score patterns
        score_patterns = [
            r'(\d+)\s*-\s*(\d+)',  # "15-3" format
            r'(\d+)\s+(\d+)',      # "15 3" format with spaces
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    score1 = int(match.group(1))
                    score2 = int(match.group(2))
                    return [score1, score2]
                except ValueError:
                    continue
        
        return []
    
    def _extract_match_type(self, element) -> MatchType:
        """Extract match type from element."""
        text = element.get_text().lower()
        
        type_mapping = {
            'pin': MatchType.PIN,
            'fall': MatchType.PIN,
            'dec': MatchType.DECISION,
            'decision': MatchType.DECISION,
            'md': MatchType.MAJOR_DECISION,
            'major': MatchType.MAJOR_DECISION,
            'tf': MatchType.TECH_FALL,
            'tech': MatchType.TECH_FALL,
            'ff': MatchType.FORFEIT,
            'forfeit': MatchType.FORFEIT,
            'dq': MatchType.DISQUALIFICATION,
            'disq': MatchType.DISQUALIFICATION,
        }
        
        for keyword, match_type in type_mapping.items():
            if keyword in text:
                return match_type
        
        return MatchType.DECISION  # Default
    
    def _extract_round_info(self, element) -> str:
        """Extract round information from element."""
        text = element.get_text().lower()
        
        round_patterns = [
            r'(round \d+)',
            r'(r\d+)',
            r'(quarterfinal|semifinal|final)',
            r'(championship|consolation)',
        ]
        
        for pattern in round_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).title()
        
        return "Unknown Round"
    
    def validate_and_clean_data(self, raw_data: dict) -> dict:
        """
        Validate and clean extracted data.
        
        Args:
            raw_data: Dictionary containing raw extracted data
            
        Returns:
            Dictionary with cleaned and validated data
        """
        cleaned_data = raw_data.copy()
        
        # Clean wrestler names
        if 'wrestler1' in cleaned_data and hasattr(cleaned_data['wrestler1'], 'name'):
            cleaned_data['wrestler1'].name = self._clean_wrestler_name(cleaned_data['wrestler1'].name)
        if 'wrestler2' in cleaned_data and hasattr(cleaned_data['wrestler2'], 'name'):
            cleaned_data['wrestler2'].name = self._clean_wrestler_name(cleaned_data['wrestler2'].name)
        
        # Validate scores
        if 'wrestler1_score' in cleaned_data:
            cleaned_data['wrestler1_score'] = max(0, int(cleaned_data.get('wrestler1_score', 0)))
        if 'wrestler2_score' in cleaned_data:
            cleaned_data['wrestler2_score'] = max(0, int(cleaned_data.get('wrestler2_score', 0)))
        
        return cleaned_data
    
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
        
        return name