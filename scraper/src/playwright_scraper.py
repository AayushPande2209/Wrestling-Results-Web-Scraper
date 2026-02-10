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
        self.base_url = "https://dubstat.com/dubstat-home/ohio-high-school-wrestling/dubstat-database/"
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
                
                # Get available genders - but only process Boys
                genders = self._get_genders(page)
                logger.info(f"Found {len(genders)} genders: {genders}")
                
                # Filter to only Boys (not Girls)
                genders_to_process = [g for g in genders if g.lower() == 'boys']
                logger.info(f"Processing only: {genders_to_process}")
                
                for gender in genders_to_process:
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
        try:
            page.goto(self.base_url, timeout=60000)  # Increase timeout to 60 seconds
            page.wait_for_load_state('domcontentloaded')  # Wait for DOM instead of networkidle
            time.sleep(3)  # Additional wait for dynamic content
            logger.info("Page loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load page: {e}")
            # Try to get page title to see if we loaded something
            try:
                title = page.title()
                logger.info(f"Page title: {title}")
            except:
                pass
            raise
        
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
            # Use the specific ID we found
            selector = '#gender'
            
            try:
                element = page.query_selector(selector)
                if element:
                    page.select_option(selector, gender)
                    logger.debug(f"Selected gender: {gender}")
                    
                    # Wait for school dropdown to populate (important!)
                    # The school dropdown gets populated via JavaScript after gender selection
                    page.wait_for_timeout(3000)  # Wait 3 seconds for AJAX to complete
                    
                    # Wait for school dropdown to have options
                    page.wait_for_function('''
                        document.querySelector('#school').options.length > 1
                    ''', timeout=10000)
                    
                    logger.debug(f"School dropdown populated after selecting {gender}")
                    return
            except Exception as e:
                logger.error(f"Error selecting gender with selector {selector}: {e}")
                    
            logger.warning(f"Could not select gender: {gender}")
            
        except Exception as e:
            logger.error(f"Error selecting gender {gender}: {e}")
    
    def _get_schools(self, page: Page) -> List[str]:
        """Get available school options for current gender."""
        try:
            # Use the specific ID we found
            selector = '#school'
            
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
                        # Filter to only include Olentangy Liberty
                        liberty_schools = [school for school in options if 'olentangy liberty' in school.lower()]
                        if liberty_schools:
                            logger.info(f"Found Olentangy Liberty school(s): {liberty_schools}")
                            return liberty_schools
                        else:
                            logger.warning("Olentangy Liberty not found in school list")
                            logger.debug(f"Available schools: {options[:10]}...")  # Show first 10 for debugging
                            return []
            except Exception as e:
                logger.error(f"Error getting schools with selector {selector}: {e}")
            
            logger.warning("Could not find school dropdown")
            return []
            
        except Exception as e:
            logger.error(f"Error getting schools: {e}")
            return []
    
    def _select_school(self, page: Page, school: str) -> None:
        """Select a school option."""
        try:
            # Use the specific ID we found
            selector = '#school'
            
            try:
                element = page.query_selector(selector)
                if element:
                    page.select_option(selector, school)
                    logger.debug(f"Selected school: {school}")
                    
                    # Wait for wrestler dropdown to populate (important!)
                    page.wait_for_timeout(3000)  # Wait 3 seconds for AJAX
                    
                    # Wait for wrestler dropdown to have options
                    page.wait_for_function('''
                        document.querySelector('#wrestler').options.length > 1
                    ''', timeout=10000)
                    
                    logger.debug(f"Wrestler dropdown populated after selecting {school}")
                    return
            except Exception as e:
                logger.error(f"Error selecting school with selector {selector}: {e}")
                    
            logger.warning(f"Could not select school: {school}")
            
        except Exception as e:
            logger.error(f"Error selecting school {school}: {e}")
    
    def _get_wrestlers(self, page: Page) -> List[str]:
        """Get available wrestler options for current school."""
        try:
            # Use the specific ID we found
            selector = '#wrestler'
            
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
            except Exception as e:
                logger.error(f"Error getting wrestlers with selector {selector}: {e}")
            
            logger.warning("Could not find wrestler dropdown")
            return []
            
        except Exception as e:
            logger.error(f"Error getting wrestlers: {e}")
            return []
    
    def _scrape_wrestler_results(self, page: Page, wrestler: str, school: str) -> List[MatchData]:
        """Scrape results for a specific wrestler."""
        try:
            # Select wrestler using the specific ID
            selector = '#wrestler'
            
            try:
                element = page.query_selector(selector)
                if element:
                    page.select_option(selector, wrestler)
                    page.wait_for_timeout(1000)
                    logger.debug(f"Selected wrestler {wrestler}")
                else:
                    logger.warning(f"Could not find wrestler dropdown")
                    return []
            except Exception as e:
                logger.error(f"Failed to select wrestler: {e}")
                return []
            
            # Click "Get Results" button using the specific ID
            button_selector = '#get-results'
            
            try:
                element = page.query_selector(button_selector)
                if element:
                    is_visible = page.is_visible(button_selector)
                    is_enabled = page.is_enabled(button_selector)
                    
                    logger.debug(f"Get Results button: visible={is_visible}, enabled={is_enabled}")
                    
                    if is_visible and is_enabled:
                        logger.debug(f"Clicking Get Results button")
                        page.click(button_selector)
                        page.wait_for_load_state('domcontentloaded')
                        time.sleep(3)  # Wait for results to load
                        logger.debug(f"Successfully clicked Get Results button")
                    else:
                        logger.warning(f"Get Results button not clickable: visible={is_visible}, enabled={is_enabled}")
                        return []
                else:
                    logger.warning(f"Could not find Get Results button")
                    return []
            except Exception as e:
                logger.error(f"Failed to click Get Results button: {e}")
                return []
            
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
        """Parse a single match row from the results table.
        
        Table structure (fixed columns):
        Column 0: Event Date
        Column 1: Event (Tournament name)
        Column 2: Round
        Column 3: Weight
        Column 4: W/L (Win/Loss)
        Column 5: Result (e.g., "D (3-0)", "F (5:32)", "TF (22-4)")
        Column 6: Opponent
        Column 7: Opponent School
        """
        try:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 8:  # Need all 8 columns
                logger.debug(f"Row has only {len(cells)} cells, expected 8")
                return None
            
            # Extract data from cells using fixed column positions
            cell_texts = [cell.get_text().strip() for cell in cells]
            
            # Column 0: Event Date (optional, not used in MVP)
            event_date = cell_texts[0] if len(cell_texts) > 0 else None
            
            # Column 1: Event (Tournament name)
            tournament_name = cell_texts[1] if len(cell_texts) > 1 else None
            if not tournament_name:
                return None
            
            # Column 2: Round
            round_info = cell_texts[2] if len(cell_texts) > 2 else "Unknown"
            
            # Column 3: Weight (not used in MVP)
            # weight = cell_texts[3] if len(cell_texts) > 3 else None
            
            # Column 4: W/L (Win/Loss)
            win_loss = cell_texts[4] if len(cell_texts) > 4 else "L"
            is_win = win_loss.upper() in ['W', 'WIN', 'WON']
            
            # Column 5: Result (e.g., "D (3-0)", "F (5:32)", "TF (22-4)")
            result_str = cell_texts[5] if len(cell_texts) > 5 else ""
            match_type, scores, match_time = self._parse_result_column(result_str)
            
            # Column 6: Opponent name
            opponent_name = cell_texts[6] if len(cell_texts) > 6 else None
            if not opponent_name:
                return None
            
            # Column 7: Opponent School (not used in MVP)
            # opponent_school = cell_texts[7] if len(cell_texts) > 7 else None
            
            # Create wrestler objects
            wrestler1 = WrestlerData(name=wrestler_name)
            wrestler2 = WrestlerData(name=opponent_name)
            
            # Determine winner and scores
            if is_win:
                winner = wrestler1
                wrestler1_score = scores.get('winner_score', 0)
                wrestler2_score = scores.get('loser_score', 0)
            else:
                winner = wrestler2
                wrestler1_score = scores.get('loser_score', 0)
                wrestler2_score = scores.get('winner_score', 0)
            
            # Parse date if available
            match_date = None
            if event_date:
                try:
                    from datetime import datetime
                    match_date = datetime.strptime(event_date, '%Y-%m-%d')
                except:
                    pass
            
            # Create match data
            match_data = MatchData(
                tournament_name=tournament_name,
                wrestler1=wrestler1,
                wrestler2=wrestler2,
                winner=winner,
                wrestler1_score=wrestler1_score,
                wrestler2_score=wrestler2_score,
                match_type=match_type,
                round=round_info,
                match_time=match_time,
                date=match_date
            )
            
            return match_data
            
        except Exception as e:
            logger.debug(f"Error parsing match row: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    def _parse_result_column(self, result_str: str) -> tuple:
        """Parse the Result column which contains match type, score, and optionally match time.
        
        Formats:
        - "D (3-0)" = Decision with score 3-0
        - "F (5:32)" = Fall/Pin at 5:32 (no score, just time)
        - "TF (22-4)" = Technical Fall with score 22-4
        - "MD (8-0)" = Major Decision with score 8-0
        - "FF" = Forfeit
        - "DQ" = Disqualification
        
        Returns:
            Tuple of (MatchType, scores_dict, match_time) where scores_dict has 'winner_score'
            and 'loser_score', and match_time is the time string for pins (e.g. "5:32") or None.
        """
        import re
        scores = {'winner_score': 0, 'loser_score': 0}
        match_time = None
        result_upper = result_str.upper().strip()
        
        # Default to decision
        match_type = MatchType.DECISION
        
        # Check for forfeit
        if 'FF' in result_upper or 'FORFEIT' in result_upper:
            match_type = MatchType.FORFEIT
            return match_type, scores, match_time
        
        # Check for disqualification
        if 'DQ' in result_upper or 'DISQUAL' in result_upper:
            match_type = MatchType.DISQUALIFICATION
            return match_type, scores, match_time
        
        # Check for fall/pin (format: "F (5:32)" or "F (1:54)")
        if result_upper.startswith('F ') or result_upper.startswith('FALL'):
            match_type = MatchType.PIN
            # Extract time from parentheses (e.g. "5:32" or "1:54.2")
            time_match = re.search(r'\((\d+:\d+(?:\.\d+)?)\)', result_str)
            if time_match:
                match_time = time_match.group(1)
            return match_type, scores, match_time
        
        # Check for technical fall (format: "TF (22-4)")
        if result_upper.startswith('TF '):
            match_type = MatchType.TECH_FALL
            # Extract score from parentheses
            score_match = re.search(r'\((\d+)-(\d+)\)', result_str)
            if score_match:
                scores['winner_score'] = int(score_match.group(1))
                scores['loser_score'] = int(score_match.group(2))
            return match_type, scores, match_time
        
        # Check for major decision (format: "MD (8-0)")
        if result_upper.startswith('MD '):
            match_type = MatchType.MAJOR_DECISION
            # Extract score from parentheses
            score_match = re.search(r'\((\d+)-(\d+)\)', result_str)
            if score_match:
                scores['winner_score'] = int(score_match.group(1))
                scores['loser_score'] = int(score_match.group(2))
            return match_type, scores, match_time
        
        # Check for decision (format: "D (3-0)")
        if result_upper.startswith('D '):
            match_type = MatchType.DECISION
            # Extract score from parentheses
            score_match = re.search(r'\((\d+)-(\d+)\)', result_str)
            if score_match:
                scores['winner_score'] = int(score_match.group(1))
                scores['loser_score'] = int(score_match.group(2))
            return match_type, scores, match_time
        
        # Fallback: try to extract any score pattern
        score_match = re.search(r'\((\d+)-(\d+)\)', result_str)
        if score_match:
            scores['winner_score'] = int(score_match.group(1))
            scores['loser_score'] = int(score_match.group(2))
        
        return match_type, scores, match_time
    
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