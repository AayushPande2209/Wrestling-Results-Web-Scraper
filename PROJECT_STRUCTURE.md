# Wrestling Analytics Platform - Project Structure

This document provides an overview of the complete project structure after setup.

## Directory Structure

```
wrestling-analytics-platform/
├── .env                           # Environment variables (configured)
├── .gitignore                     # Git ignore rules
├── README.md                      # Main project documentation
├── PROJECT_STRUCTURE.md           # This file
├── setup.sh                       # Automated setup script
├── scraper.py                     # Original scraper (legacy)
│
├── scraper/                       # Python web scraper component
│   ├── README.md                  # Scraper documentation
│   ├── requirements.txt           # Python dependencies
│   ├── src/                       # Source code (to be implemented)
│   │   └── __init__.py
│   ├── config/                    # Configuration modules
│   │   ├── __init__.py
│   │   └── settings.py            # Settings management
│   └── tests/                     # Unit and property-based tests (to be created)
│
├── dashboard/                     # Next.js web dashboard
│   ├── README.md                  # Dashboard documentation
│   ├── package.json               # Node.js dependencies
│   ├── next.config.js             # Next.js configuration
│   ├── tsconfig.json              # TypeScript configuration
│   ├── tailwind.config.js         # Tailwind CSS configuration
│   ├── src/                       # Source code
│   │   ├── types/                 # TypeScript type definitions
│   │   │   └── database.ts        # Database schema types
│   │   └── utils/                 # Utility functions
│   │       └── supabase.ts        # Supabase client configuration
│   ├── components/                # React components (to be implemented)
│   ├── pages/                     # Next.js pages (to be implemented)
│   └── hooks/                     # Custom React hooks (to be implemented)
│
├── shared/                        # Shared configuration and utilities
│   ├── README.md                  # Shared components documentation
│   ├── database/                  # Database schema and setup
│   │   ├── schema.sql             # Main database schema
│   │   ├── rls_policies.sql       # Row Level Security policies
│   │   ├── realtime_config.sql    # Real-time subscriptions setup
│   │   ├── setup.sql              # Complete setup script
│   │   └── init_dev_data.sql      # Development sample data
│   └── config/                    # Environment configuration templates
│       ├── .env.template          # Environment variables template
│       ├── .env.development       # Development configuration
│       └── .env.production        # Production configuration
│
└── .kiro/                         # Kiro IDE specifications
    └── specs/
        └── wrestling-analytics-platform/
            ├── requirements.md     # Project requirements
            ├── design.md          # System design document
            └── tasks.md           # Implementation tasks
```

## Component Overview

### 1. Python Scraper (`scraper/`)
- **Purpose**: Extract wrestling match data from DubStat
- **Key Features**: 
  - HTML parsing with BeautifulSoup
  - Data validation and cleaning
  - Supabase database integration
  - Error handling with retry logic
  - FastAPI endpoints for manual triggering

### 2. Next.js Dashboard (`dashboard/`)
- **Purpose**: Real-time web interface for viewing analytics
- **Key Features**:
  - Real-time data updates via Supabase
  - Responsive design with Tailwind CSS
  - TypeScript for type safety
  - Wrestling analytics and statistics
  - Scraper control panel

### 3. Shared Configuration (`shared/`)
- **Purpose**: Common configuration and database schema
- **Key Features**:
  - Complete PostgreSQL schema
  - Row Level Security policies
  - Real-time subscription configuration
  - Environment-specific configurations

### 4. Database Schema
The system uses 5 main tables:
- `teams` - Wrestling teams and schools
- `tournaments` - Tournament information
- `wrestlers` - Individual wrestler profiles
- `matches` - Match results and scores
- `scraper_jobs` - Scraping job tracking

## Setup Status

✅ **Completed:**
- Project directory structure
- Database schema with constraints and indexes
- Row Level Security policies
- Real-time subscriptions configuration
- Environment configuration templates
- Python scraper configuration
- Next.js dashboard foundation
- TypeScript type definitions
- Development and production configurations

🔄 **Next Steps (Remaining Tasks):**
- Implement Python scraper classes (DubStatScraper, HTMLParser, etc.)
- Create FastAPI endpoints for scraper control
- Build React components for dashboard
- Implement real-time hooks and data fetching
- Add comprehensive testing (unit and property-based)
- Set up deployment configurations

## Quick Start

1. **Database Setup**: Run SQL scripts in Supabase in this order:
   - `shared/database/schema.sql`
   - `shared/database/rls_policies.sql`
   - `shared/database/realtime_config.sql`
   - `shared/database/init_dev_data.sql` (optional)

2. **Environment**: Update `.env` with your Supabase credentials

3. **Dependencies**: 
   ```bash
   # Python scraper
   cd scraper && pip install -r requirements.txt
   
   # Next.js dashboard
   cd dashboard && npm install
   ```

4. **Development**:
   ```bash
   # Dashboard
   cd dashboard && npm run dev
   
   # Scraper API (when implemented)
   cd scraper && python -m uvicorn src.api:app --reload
   ```

## Configuration Files

- `.env` - Main environment variables (configured with your Supabase project)
- `shared/config/.env.development` - Development-specific settings
- `shared/config/.env.production` - Production-specific settings
- `shared/config/.env.template` - Template for new environments

## Database Connection

Your Supabase project is configured:
- **URL**: `https://qsncbvjopbennwsxxkyi.supabase.co`
- **Environment**: Development
- **Real-time**: Enabled for all tables
- **Security**: RLS policies configured for public read, authenticated write

The project structure is now complete and ready for implementation of the remaining tasks!