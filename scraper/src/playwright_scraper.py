"""
Playwright-based DubStat scraper for wrestling analytics.
Implements Gender → School → Wrestler → Results loop.
"""
import time
import logging
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright, Page, Browser
from bs4 import BeautifulSoup
from datetime import datetime

from .models import WrestlerData, MatchData, TournamentData, MatchType
from .supabase_client import SupabaseClient
from .data_validator import DataValidator


logger = logging.getLogger(__name__)


class PlaywrightScraper:
    """Playwright-based scraper for DubStat wrestling database."""
    
    def __init__(self, headless: bool = True):
        """Initialize the scraper."""
        self.headless = headless
        self.base_url = "https://www.dubstat.com/database"
        self.db_client = SupabaseClient()
        self.validator = DataValidator()
        
    def scrape_all_data(self) -> Dict[str, Any]:
        """
        Main scraping function that loops through all data.
        Returns summary statistics.
        """
        logger.info("🏆 Starting complete DubStat scraping...")
        
        stats = {
            'total_matches': 0,
            'total_wrestlers': 0,
            'total_schools': 0,
            'successful_inserts': 0,
            'errors': 0,
            'start_time': datetime.now(),
            'end_time': None
        }
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            
            try:
                # Load the database page
                self._load_page(page)
                
                # Get available genders
                genders = self._get_genders(page)
                logger.info(f"Found {len(genders)} genders: {genders}")
                
                for gender in genders:
                    logger.info(f"🚹 Processing gender: {gender}")
                    
                    # Select gender
                    self._select_gender(page, gender)
                    
                    # Get schools for this gender
                    schools = self._get_schools(page)
                    logger.info(f"Found {len(schools)} schools for {gender}")
                    stats['total_schools'] += len(schools)
                    
                    for school in schools:
                        logger.info(f"🏫 Processing school: {school}")
                        
                        try:
                            # Select school
                            self._select_school(page, school)
                            
                            # Get wrestlers for this school
                            wrestlers = self._get_wrestlers(page)
                            logger.info(f"Found {len(wrestlers)} wrestlers at {school}")
                            stats['total_wrestlers'] += len(wrestlers)
                            
                            for wrestler in wrestlers:
                                logger.info(f"🤼 Processing wrestler: {wrestler}")
                                
                                try:
                                    # Scrape this wrestler's results
                                    matches = self._scrape_wrestler_results(page, wrestler, school)
                                    stats['total_matches'] += len(matches)
                                    
                                    # Insert matches into database
                                    if matches:
                                        success = self.db_client.batch_insert_matches(matches)
                                        if success:
                                            stats['successful_inserts'] += len(matches)
                                        else:
                                            stats['errors'] += len(matches)
                                    
                                except Exception as e:
                                    logger.error(f"Error processing wrestler {wrestler}: {e}")
                                    stats['errors'] += 1
                                    continue
                                    
                        except Exception as e:
                            logger.error(f"Error processing school {school}: {e}")
                            stats['errors'] += 1
                            continue
                            
            except Exception as e:
                logger.error(f"Critical scraping error: {e}")
                raise
            finally:
                browser.close()
                stats['end_time'] = datetime.now()
                
        return stats
    
    def _load_page(self, page: Page) -> None:
        """Load the DubStat database page."""
        logger.info(f"Loading page: {self.base_url}")
        page.goto(self.base_url)
        page.wait_for_load_state('networkidle')
        time.sleep(2)  # Additional wait for dynamic content
        
    def _get_genders(self, page: Page) -> List[str]:
        """Get available gender options."""
        try:
            # Look for gender dropdown/select
            gender_selectors = [
                'select[name*="gender"]',
                'select[id*="gender"]',
                '#gender',
                '.gender-select',
                'select:has(option[value*="male"])',
                'select:has(option[value*="boy"])',
                'select:has(option[value*="girl"])'
            ]
            
            for selector in gender_selectors:
                try:
                    element = page.wait_for_selector(selector, timeout=5000)
                    if element:
                        # Get all option values
                        options = page.evaluate(f'''
                            Array.from(document.querySelector("{selector}").options)
                                .map(option => option.value)
                                .filter(value => value && value !== "")
                        ''')
                        if options:
                            logger.debug(f"Found genders using selector {selector}: {options}")
                            return options
                except:
                    continue
            
            # Fallback: common gender values
            logger.warning("Could not find gender dropdown, using defaults")
            return ['boys', 'girls']
            
        except Exception as e:
            logger.error(f"Error getting genders: {e}")
            return ['boys', 'girls']  # Default fallback
    
    def _select_gender(self, page: Page, gender: str) -> None:
        """Select a gender option."""
        try:
            gender_selectors = [
                'select[name*="gender"]',
                'select[id*="gender"]',
                '#gender',
                '.gender-select'
            ]
            
            for selector in gender_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        page.select_option(selector, gender)
                        page.wait_for_timeout(1000)  # Wait for page to update
                        logger.debug(f"Selected gender: {gender}")
                        return
                except:
                    continue
                    
            logger.warning(f"Could not select gender: {gender}")
            
        except Exception as e:
            logger.error(f"Error selecting gender {gender}: {e}")
    
    def _get_schools(self, page: Page) -> List[str]:
        """Get available school options for current gender."""
        try:
            # Look for school dropdown
            school_selectors = [
                'select[name*="school"]',
                'select[id*="school"]',
                '#school',
                '.school-select',
                'select:has(option[value*="high"])',
                'select:has(option[value*="school"])'
            ]
            
            for selector in school_selectors:
                try:
                    element = page.wait_for_selector(selector, timeout=5000)
                    if element:
                        # Get all option values, excluding empty ones
                        options = page.evaluate(f'''
                            Array.from(document.querySelector("{selector}").options)
                                .map(option => option.value)
                                .filter(value => value && value !== "" && value !== "0")
                        ''')
                        if options:
                            logger.debug(f"Found {len(options)} schools")
                            return options[:50]  # Limit for testing - remove in production
                except:
                    continue
            
            logger.warning("Could not find school dropdown")
            return []
            
        except Exception as e:
            logger.error(f"Error getting schools: {e}")
            return []
    
    def _select_school(self, page: Page, school: str) -> None:
        """Select a school option."""
        try:
            school_selectors = [
                'select[name*="school"]',
                'select[id*="school"]',
                '#school',
                '.school-select'
            ]
            
            for selector in school_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        page.select_option(selector, school)
                        page.wait_for_timeout(2000)  # Wait for wrestler dropdown to populate
                        logger.debug(f"Selected school: {school}")
                        return
                except:
                    continue
                    
            logger.warning(f"Could not select school: {school}")
            
        except Exception as e:
            logger.error(f"Error selecting school {school}: {e}")
    
    def _get_wrestlers(self, page: Page) -> List[str]:
        """Get available wrestler options for current school."""
        try:
            # Look for wrestler dropdown
            wrestler_selectors = [
                'select[name*="wrestler"]',
                'select[id*="wrestler"]',
                '#wrestler',
                '.wrestler-select',
                'select[name*="athlete"]',
                'select[id*="athlete"]'
            ]
            
            for selector in wrestler_selectors:
                try:
                    element = page.wait_for_selector(selector, timeout=5000)
                    if element:
                        # Get all option values, excluding empty ones
                        options = page.evaluate(f'''
                            Array.from(document.querySelector("{selector}").options)
                                .map(option => option.value)
                                .filter(value => value && value !== "" && value !== "0")
                        ''')
                        if options:
                            logger.debug(f"Found {len(options)} wrestlers")
                            return options
                except:
                    continue
            
            logger.warning("Could not find wrestler dropdown")
            return []
            
        except Exception as e:
            logger.error(f"Error getting wrestlers: {e}")
            return []
    
    def _scrape_wrestler_results(self, page: Page, wrestler: str, school: str) -> List[MatchData]:
        """Scrape results for a specific wrestler."""
        try:
            # Select wrestler
            wrestler_selectors = [
                'select[name*="wrestler"]',
                'select[id*="wrestler"]',
                '#wrestler',
                '.wrestler-select'
            ]
            
            for selector in wrestler_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        page.select_option(selector, wrestler)
                        page.wait_for_timeout(1000)
                        break
                except:
                    continue
            
            # Click "Get Results" button
            result_button_selectors = [
                'input[type="submit"][value*="Results"]',
                'button:has-text("Get Results")',
                'input[value*="Get Results"]',
                '.get-results',
                '#get-results'
            ]
            
            for selector in result_button_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        page.click(selector)
                        page.wait_for_load_state('networkidle')
                        time.sleep(2)  # Wait for results to load
                        break
                except:
                    continue
            
            # Get the results table HTML
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Parse matches from the results table
            matches = self._parse_results_table(soup, wrestler, school)
            
            logger.info(f"Found {len(matches)} matches for {wrestler}")
            return matches
            
        except Exception as e:
            logger.error(f"Error scraping results for wrestler {wrestler}: {e}")
            return []
    
    def _parse_results_table(self, soup: BeautifulSoup, wrestler_name: str, school: str) -> List[MatchData]:
        """Parse matches from the results table HTML."""
        matches = []
        
        try:
            # Look for results table
            table_selectors = [
                'table.results',
                'table#results',
                '.results-table',
                'table:has(th:contains("Tournament"))',
                'table:has(th:contains("Opponent"))',
                'table:has(td:contains("vs"))'
            ]
            
            results_table = None
            for selector in table_selectors:
                results_table = soup.select_one(selector)
                if results_table:
                    break
            
            if not results_table:
                # Fallback: find any table with match-like data
                tables = soup.find_all('table')
                for table in tables:
                    if self._looks_like_results_table(table):
                        results_table = table
                        break
            
            if not results_table:
                logger.warning(f"No results table found for {wrestler_name}")
                return matches
            
            # Parse table rows
            rows = results_table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                try:
                    match_data = self._parse_match_row(row, wrestler_name, school)
                    if match_data:
                        matches.append(match_data)
                except Exception as e:
                    logger.debug(f"Error parsing row: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error parsing results table: {e}")
        
        return matches
    
    def _looks_like_results_table(self, table) -> bool:
        """Check if a table looks like it contains match results."""
        text = table.get_text().lower()
        indicators = ['tournament', 'opponent', 'result', 'score', 'vs', 'win', 'loss']
        return sum(1 for indicator in indicators if indicator in text) >= 3
    
    def _parse_match_row(self, row, wrestler_name: str, school: str) -> Optional[MatchData]:
        """Parse a single match row from the results table."""
        try:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 4:  # Need at least tournament, opponent, result, score
                return None
            
            # Extract data from cells (order may vary by site)
            cell_texts = [cell.get_text().strip() for cell in cells]
            
            # Try to identify columns by content patterns
            tournament_name = self._extract_tournament_from_cells(cell_texts)
            opponent_info = self._extract_opponent_from_cells(cell_texts)
            result_info = self._extract_result_from_cells(cell_texts)
            score_info = self._extract_score_from_cells(cell_texts)
            
            if not all([tournament_name, opponent_info, result_info]):
                return None
            
            # Create wrestler objects
            wrestler1 = WrestlerData(name=wrestler_name, team=school)
            wrestler2 = WrestlerData(name=opponent_info['name'], team=opponent_info.get('team', 'Unknown'))
            
            # Determine winner and scores
            if result_info['result'].lower() in ['w', 'win', 'won']:
                winner = wrestler1
                wrestler1_score = score_info.get('winner_score', 0)
                wrestler2_score = score_info.get('loser_score', 0)
            else:
                winner = wrestler2
                wrestler1_score = score_info.get('loser_score', 0)
                wrestler2_score = score_info.get('winner_score', 0)
            
            # Create match data
            match_data = MatchData(
                tournament_name=tournament_name,
                wrestler1=wrestler1,
                wrestler2=wrestler2,
                winner=winner,
                wrestler1_score=wrestler1_score,
                wrestler2_score=wrestler2_score,
                match_type=self._parse_match_type(result_info.get('type', '')),
                round=result_info.get('round', 'Unknown'),
                date=None  # Will be extracted if available
            )
            
            return match_data
            
        except Exception as e:
            logger.debug(f"Error parsing match row: {e}")
            return None
    
    def _extract_tournament_from_cells(self, cells: List[str]) -> str:
        """Extract tournament name from table cells."""
        for cell in cells:
            # Tournament names often contain words like "tournament", "invitational", "classic"
            if any(word in cell.lower() for word in ['tournament', 'invitational', 'classic', 'dual', 'meet']):
                return cell
        
        # Fallback: first non-empty cell that's not obviously something else
        for cell in cells:
            if cell and not any(pattern in cell.lower() for pattern in ['vs', 'w-', 'l-', 'pin', 'dec']):
                return cell
        
        return "Unknown Tournament"
    
    def _extract_opponent_from_cells(self, cells: List[str]) -> Dict[str, str]:
        """Extract opponent information from table cells."""
        for cell in cells:
            if 'vs' in cell.lower() or ' v ' in cell.lower():
                # Parse "vs Opponent Name (Team)" format
                parts = cell.replace('vs', '').replace('v', '').strip()
                if '(' in parts and ')' in parts:
                    name = parts.split('(')[0].strip()
                    team = parts.split('(')[1].split(')')[0].strip()
                    return {'name': name, 'team': team}
                else:
                    return {'name': parts, 'team': 'Unknown'}
        
        # Look for names (capitalized words)
        for cell in cells:
            if cell and cell[0].isupper() and ' ' in cell and len(cell.split()) >= 2:
                return {'name': cell, 'team': 'Unknown'}
        
        return {'name': 'Unknown Opponent', 'team': 'Unknown'}
    
    def _extract_result_from_cells(self, cells: List[str]) -> Dict[str, str]:
        """Extract match result information from table cells."""
        result_info = {'result': 'L', 'type': '', 'round': ''}
        
        for cell in cells:
            cell_lower = cell.lower()
            
            # Check for win/loss
            if cell_lower in ['w', 'win', 'won']:
                result_info['result'] = 'W'
            elif cell_lower in ['l', 'loss', 'lost']:
                result_info['result'] = 'L'
            
            # Check for match type
            if 'pin' in cell_lower or 'fall' in cell_lower:
                result_info['type'] = 'pin'
            elif 'dec' in cell_lower:
                result_info['type'] = 'decision'
            elif 'md' in cell_lower or 'major' in cell_lower:
                result_info['type'] = 'major_decision'
            elif 'tf' in cell_lower or 'tech' in cell_lower:
                result_info['type'] = 'tech_fall'
            
            # Check for round info
            if 'final' in cell_lower:
                result_info['round'] = 'Final'
            elif 'semi' in cell_lower:
                result_info['round'] = 'Semifinal'
            elif 'quarter' in cell_lower:
                result_info['round'] = 'Quarterfinal'
        
        return result_info
    
    def _extract_score_from_cells(self, cells: List[str]) -> Dict[str, int]:
        """Extract score information from table cells."""
        scores = {'winner_score': 0, 'loser_score': 0}
        
        for cell in cells:
            # Look for score patterns like "15-3", "21-6", etc.
            import re
            score_match = re.search(r'(\d+)-(\d+)', cell)
            if score_match:
                score1, score2 = int(score_match.group(1)), int(score_match.group(2))
                # Assume higher score is winner
                if score1 > score2:
                    scores['winner_score'] = score1
                    scores['loser_score'] = score2
                else:
                    scores['winner_score'] = score2
                    scores['loser_score'] = score1
                break
        
        return scores
    
    def _parse_match_type(self, type_str: str) -> MatchType:
        """Parse match type from string."""
        type_lower = type_str.lower()
        
        if 'pin' in type_lower or 'fall' in type_lower:
            return MatchType.PIN
        elif 'md' in type_lower or 'major' in type_lower:
            return MatchType.MAJOR_DECISION
        elif 'tf' in type_lower or 'tech' in type_lower:
            return MatchType.TECH_FALL
        elif 'dec' in type_lower:
            return MatchType.DECISION
        elif 'ff' in type_lower or 'forfeit' in type_lower:
            return MatchType.FORFEIT
        elif 'dq' in type_lower:
            return MatchType.DISQUALIFICATION
        else:
            return MatchType.DECISION  # Default