# Requirements Document - Wrestling Analytics MVP

## Introduction

The Wrestling Analytics Platform is a simple data pipeline that scrapes wrestling match data from DubStat, stores it in Supabase, and displays analytics through a web dashboard. This MVP focuses on core functionality: data collection, basic analytics, and visualization for high school wrestling teams.

## Glossary

- **Scraper**: Python script that extracts match data from DubStat
- **Dashboard**: Next.js web app for viewing wrestler and team analytics
- **DubStat**: Wrestling statistics website (data source)
- **Match**: Individual wrestling bout with participants and outcome
- **Tournament**: Collection of matches at a competition
- **Wrestler**: Individual competitor with performance stats

## MVP Requirements

### Requirement 1: Data Collection

**User Story:** As a wrestling coach, I want to collect match data from DubStat so I can analyze my wrestlers' performance.

#### Acceptance Criteria

1. Python scraper can extract wrestler names, teams, match scores, and tournament info from DubStat pages
2. Scraper handles basic parsing errors gracefully (skip bad data, continue processing)
3. Extracted data is stored in Supabase database with proper relationships
4. Basic duplicate prevention prevents the same match from being inserted twice
5. Scraper can be run manually via command line

### Requirement 2: Data Storage

**User Story:** As a system user, I want match data stored reliably so I can access historical performance.

#### Acceptance Criteria

1. Database stores wrestlers with names, teams, and basic info
2. Database stores matches with participants, scores, outcomes, and tournament
3. Database maintains relationships between wrestlers, matches, and tournaments
4. Data integrity is maintained (no orphaned records)

### Requirement 3: Wrestling Analytics

**User Story:** As a coach, I want to see wrestler performance metrics so I can track improvement.

#### Acceptance Criteria

1. System calculates win-loss records and win percentages for each wrestler
2. System tracks scoring averages and recent performance trends
3. System shows head-to-head records between wrestlers
4. System provides team-level statistics (team win %, top performers)

### Requirement 4: Dashboard Display

**User Story:** As a user, I want a web dashboard to view wrestling analytics easily.

#### Acceptance Criteria

1. Dashboard displays wrestler profiles with stats and match history
2. Dashboard shows tournament results and standings
3. Dashboard provides search and filtering for wrestlers and teams
4. Dashboard is responsive and works on mobile devices
5. Dashboard loads quickly with reasonable performance

### Requirement 5: Basic Data Quality

**User Story:** As a developer, I want basic data validation so the system handles bad data gracefully.

#### Acceptance Criteria

1. Invalid wrestler names or scores are logged and skipped
2. System validates weight classes against standard wrestling weights
3. System handles missing or malformed tournament data
4. Basic error logging helps with debugging issues