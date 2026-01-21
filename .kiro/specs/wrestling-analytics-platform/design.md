# Design Document: Wrestling Analytics MVP

## Overview

The Wrestling Analytics Platform is a simple three-component system: a Python scraper, Supabase database, and Next.js dashboard. The scraper extracts wrestling data from DubStat, stores it in PostgreSQL via Supabase, and the dashboard displays analytics and statistics.

This MVP focuses on core functionality with minimal complexity - no real-time features, job queues, or enterprise infrastructure. The goal is a working analytics system that can be built and shipped by a student developer.

## Architecture

### Simple Pipeline Architecture

```
DubStat Website → Python Scraper → Supabase Database → Next.js Dashboard
```

**Data Flow:**
1. **Extract**: Python script scrapes DubStat HTML pages
2. **Transform**: BeautifulSoup parses HTML and validates data
3. **Load**: Direct insertion into Supabase PostgreSQL
4. **Display**: Next.js dashboard queries database and shows analytics

### Deployment Strategy

- **Scraper**: Run locally or on simple cloud instance (manual execution)
- **Database**: Supabase hosted PostgreSQL with web interface
- **Dashboard**: Vercel deployment with automatic builds
- **Configuration**: Simple .env files for credentials

## Components

### Python Scraper

**Purpose**: Extract match data from DubStat and insert into database

**Core Files:**
- `scraper.py` - Main script with scraping logic
- `models.py` - Data classes for wrestlers, matches, tournaments
- `database.py` - Supabase client and insertion logic
- `requirements.txt` - Python dependencies

**Key Functions:**
```python
def scrape_tournament(url: str) -> List[Match]:
    """Scrape a tournament page and return match data"""

def insert_matches(matches: List[Match]) -> int:
    """Insert matches into database, return count inserted"""

def main():
    """Main scraper entry point - run from command line"""
```

**Usage:**
```bash
python scraper.py --url "https://dubstat.com/tournament/123"
```

### Supabase Database

**Purpose**: Store wrestling data with proper relationships and constraints

**Tables:**
```sql
-- Core tables only
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    school VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE wrestlers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    team_id UUID REFERENCES teams(id),
    weight_class INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tournaments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    date DATE,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tournament_id UUID REFERENCES tournaments(id),
    wrestler1_id UUID REFERENCES wrestlers(id),
    wrestler2_id UUID REFERENCES wrestlers(id),
    winner_id UUID REFERENCES wrestlers(id),
    wrestler1_score INTEGER,
    wrestler2_score INTEGER,
    match_type VARCHAR(50),
    round VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Key Features:**
- Simple foreign key relationships
- Basic constraints and validation
- No complex triggers or stored procedures
- Standard PostgreSQL features only

### Next.js Dashboard

**Purpose**: Display wrestling analytics in a clean, responsive web interface

**Pages:**
- `/` - Home page with overview stats
- `/wrestlers` - List of all wrestlers with basic stats
- `/wrestlers/[id]` - Individual wrestler profile
- `/tournaments` - List of tournaments
- `/tournaments/[id]` - Tournament results and brackets
- `/teams` - Team rankings and stats

**Key Components:**
```typescript
// Simple React components
function WrestlerCard({ wrestler }) {
  return (
    <div className="card">
      <h3>{wrestler.name}</h3>
      <p>{wrestler.record} ({wrestler.winPercentage}%)</p>
    </div>
  )
}

function TournamentResults({ tournament }) {
  return (
    <div>
      <h2>{tournament.name}</h2>
      <MatchList matches={tournament.matches} />
    </div>
  )
}
```

**Data Fetching:**
- Simple API routes in Next.js
- Direct Supabase queries (no complex caching)
- Server-side rendering for SEO
- Client-side navigation for speed

## Data Models

### Core Data Structures

**Simplified Models:**
```python
@dataclass
class Wrestler:
    name: str
    team: str
    weight_class: Optional[int] = None

@dataclass
class Match:
    tournament: str
    wrestler1: Wrestler
    wrestler2: Wrestler
    winner: Optional[Wrestler]
    wrestler1_score: int
    wrestler2_score: int
    match_type: str
    round: str

@dataclass
class Tournament:
    name: str
    date: Optional[datetime]
    location: Optional[str]
    matches: List[Match]
```

### Analytics Calculations

**Basic Wrestling Stats:**
```python
def calculate_wrestler_stats(wrestler_id: str) -> dict:
    """Calculate basic wrestler statistics"""
    matches = get_wrestler_matches(wrestler_id)
    
    wins = sum(1 for m in matches if m.winner_id == wrestler_id)
    losses = len(matches) - wins
    win_pct = wins / len(matches) if matches else 0
    
    return {
        'wins': wins,
        'losses': losses,
        'win_percentage': win_pct,
        'total_matches': len(matches)
    }

def calculate_team_stats(team_id: str) -> dict:
    """Calculate team-level statistics"""
    wrestlers = get_team_wrestlers(team_id)
    
    total_wins = sum(w.wins for w in wrestlers)
    total_matches = sum(w.total_matches for w in wrestlers)
    
    return {
        'team_win_percentage': total_wins / total_matches if total_matches else 0,
        'total_wrestlers': len(wrestlers),
        'active_wrestlers': len([w for w in wrestlers if w.total_matches > 0])
    }
```

## Error Handling

### Simple Error Strategy

**Scraper Errors:**
- Log errors to console/file
- Skip bad data and continue
- Basic retry for network failures (3 attempts max)
- Graceful degradation

**Database Errors:**
- Log connection issues
- Skip duplicate inserts
- Basic constraint violation handling
- No complex recovery logic

**Dashboard Errors:**
- Show error messages to user
- Fallback to cached data when possible
- Basic loading states
- Simple error boundaries

## Testing Strategy

### Minimal Testing Approach

**Unit Tests:**
- Test core parsing logic with sample HTML
- Test analytics calculations with known data
- Test database insertion with mock data
- Focus on critical business logic only

**Integration Tests:**
- Test full scraper pipeline with sample tournament
- Test dashboard with sample database
- Manual testing for UI/UX validation

**No Property-Based Testing:**
- Keep tests simple and focused
- Use realistic sample data
- Manual testing for edge cases
- Focus on shipping over comprehensive testing

## Development Phases

### Phase 1: Data Pipeline (Week 1-2)
- Set up Supabase database
- Build basic scraper with BeautifulSoup
- Test with sample tournament data
- Verify data insertion works

### Phase 2: Analytics (Week 3)
- Implement wrestler statistics calculations
- Add team-level analytics
- Create basic data validation
- Test analytics accuracy

### Phase 3: Dashboard (Week 4-5)
- Build Next.js app with basic pages
- Connect to Supabase
- Display wrestler and tournament data
- Add search and filtering

### Phase 4: Polish & Deploy (Week 6)
- Improve UI/UX
- Add responsive design
- Deploy to Vercel
- Document usage and setup

### Future Enhancements (Post-MVP)
- Real-time updates
- Advanced analytics
- User authentication
- Mobile app
- Automated scraping
- Performance optimizations