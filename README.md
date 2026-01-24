# Wrestling Analytics Platform

A comprehensive system for scraping, storing, and analyzing wrestling match data from DubStat. The platform consists of a Python web scraper, Supabase backend, and Next.js dashboard with real-time updates.

## Project Structure

```
wrestling-analytics-platform/
├── scraper/                 # Python web scraper
│   ├── src/                # Source code
│   ├── config/             # Configuration files
│   ├── tests/              # Unit and property-based tests
│   └── requirements.txt    # Python dependencies
├── dashboard/              # Next.js web dashboard
│   ├── src/                # Source code
│   ├── components/         # React components
│   ├── pages/              # Next.js pages
│   └── package.json        # Node.js dependencies
├── shared/                 # Shared configuration
│   ├── database/           # Database schema and migrations
│   └── config/             # Environment configuration
└── README.md               # This file
```

## Features

- **Automated Data Scraping**: Extract wrestling match data from DubStat
- **Real-time Dashboard**: Live updates of match results and statistics
- **Comprehensive Analytics**: Wrestler performance metrics and team statistics
- **Robust Error Handling**: Resilient scraping with retry logic and data validation
- **Property-Based Testing**: Formal correctness verification using PBT

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Supabase account
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wrestling-analytics-platform
   ```

2. **Set up Supabase database**
   - Create a new Supabase project
   - Run the SQL scripts in `shared/database/` in order:
     - `schema_mvp.sql` - Create tables and constraints
     - `rls_policies.sql` - Set up Row Level Security (optional for MVP)
     - `realtime_config.sql` - Configure real-time subscriptions (optional for MVP)
     - `init_dev_data_mvp.sql` - Add sample data (optional)

3. **Configure environment variables**
   ```bash
   # Copy template and fill in your values
   cp shared/config/.env.template .env
   
   # Or use environment-specific configs
   cp shared/config/.env.development .env  # For development
   cp shared/config/.env.production .env   # For production
   ```

4. **Set up Python scraper**
   ```bash
   cd scraper
   pip install -r requirements.txt
   ```

5. **Set up Next.js dashboard**
   ```bash
   cd dashboard
   npm install
   ```

### Running the Application

1. **Manual scraper usage** (recommended for MVP)
   ```bash
   cd scraper
   # Quick start with simple scraper
   python ../scraper.py
   
   # Or use the advanced scraper with specific tournament
   python run_scraper.py https://www.dubstat.com/tournament/12345
   ```

2. **Start the scraper API** (optional, for automated scraping)
   ```bash
   cd scraper
   python -m uvicorn src.api:app --reload
   ```

3. **Start the dashboard**
   ```bash
   cd dashboard
   npm run dev
   ```

4. **Access the application**
   - Dashboard: http://localhost:3000
   - Scraper API: http://localhost:8000

## Manual Scraper Usage

The scraper can be run manually to collect wrestling data from DubStat tournaments:

### Quick Start
```bash
# Simple scraping (edit scraper.py to change URL)
python scraper.py

# Advanced scraping with custom URL
cd scraper
python run_scraper.py https://www.dubstat.com/tournament/your-tournament-id
```

### Finding Tournament URLs
1. Visit [DubStat.com](https://www.dubstat.com)
2. Navigate to tournaments or search for your team
3. Copy the tournament page URL
4. Use the URL with the scraper

### Troubleshooting
If you encounter issues with the scraper:
- See `scraper/README.md` for detailed usage instructions
- Check `SCRAPER_TROUBLESHOOTING.md` for common problems and solutions
- Ensure your Supabase environment variables are configured correctly

## Environment Variables

Key environment variables (see `shared/config/.env.template` for complete list):

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key
- `SUPABASE_SERVICE_ROLE_KEY` - Supabase service role key (for scraper)
- `NEXT_PUBLIC_SUPABASE_URL` - Public Supabase URL for dashboard
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Public Supabase key for dashboard

## Database Schema

The platform uses five main tables:

- **teams** - Wrestling teams and schools
- **tournaments** - Tournament information
- **wrestlers** - Individual wrestler profiles
- **matches** - Match results and scores
- **scraper_jobs** - Scraping job tracking

See `shared/database/schema_mvp.sql` for complete schema definition.

## Development

### Running Tests

**Python tests:**
```bash
cd scraper
pytest tests/
```

**Property-based tests:**
```bash
cd scraper
pytest tests/ -k "property"
```

### Code Quality

**Python linting:**
```bash
cd scraper
flake8 src/
black src/
```

**TypeScript checking:**
```bash
cd dashboard
npm run type-check
npm run lint
```

## Deployment

### Dashboard (Vercel)

1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Scraper (Railway/Heroku)

1. Create new app on Railway or Heroku
2. Set environment variables
3. Deploy from repository

### Database (Supabase)

1. Create production Supabase project
2. Run database scripts
3. Configure production environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open a GitHub issue or contact the development team.