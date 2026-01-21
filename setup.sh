#!/bin/bash

# Wrestling Analytics Platform Setup Script
# This script helps set up the development environment

set -e

echo "🤼 Wrestling Analytics Platform Setup"
echo "===================================="

# Check if required tools are installed
check_requirements() {
    echo "Checking requirements..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is required but not installed."
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is required but not installed."
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "❌ npm is required but not installed."
        exit 1
    fi
    
    echo "✅ All requirements satisfied"
}

# Set up environment variables
setup_env() {
    echo "Setting up environment variables..."
    
    if [ ! -f .env ]; then
        echo "📝 Creating .env file from template..."
        cp shared/config/.env.development .env
        echo "⚠️  Please edit .env file with your actual Supabase credentials"
    else
        echo "✅ .env file already exists"
    fi
}

# Set up Python scraper
setup_scraper() {
    echo "Setting up Python scraper..."
    
    cd scraper
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "🐍 Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment and install dependencies
    echo "📦 Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create logs directory
    mkdir -p logs
    
    cd ..
    echo "✅ Python scraper setup complete"
}

# Set up Next.js dashboard
setup_dashboard() {
    echo "Setting up Next.js dashboard..."
    
    cd dashboard
    
    # Install Node.js dependencies
    echo "📦 Installing Node.js dependencies..."
    npm install
    
    # Create necessary directories
    mkdir -p src/components
    mkdir -p src/hooks
    mkdir -p src/pages
    mkdir -p src/utils
    
    cd ..
    echo "✅ Next.js dashboard setup complete"
}

# Create necessary directories
create_directories() {
    echo "Creating project directories..."
    
    # Create logs directory
    mkdir -p logs
    
    # Create test directories
    mkdir -p scraper/tests
    mkdir -p dashboard/tests
    
    echo "✅ Directories created"
}

# Display next steps
show_next_steps() {
    echo ""
    echo "🎉 Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your Supabase credentials"
    echo "2. Set up your Supabase database:"
    echo "   - Create a new Supabase project"
    echo "   - Run the SQL scripts in shared/database/ in your Supabase SQL editor:"
    echo "     a. schema.sql"
    echo "     b. rls_policies.sql"
    echo "     c. realtime_config.sql"
    echo "     d. init_dev_data.sql (optional, for sample data)"
    echo ""
    echo "3. Start the development servers:"
    echo "   Dashboard: cd dashboard && npm run dev"
    echo "   Scraper API: cd scraper && source venv/bin/activate && python -m uvicorn src.api:app --reload"
    echo ""
    echo "4. Access the application:"
    echo "   Dashboard: http://localhost:3000"
    echo "   Scraper API: http://localhost:8000"
    echo ""
    echo "For more information, see README.md"
}

# Main setup process
main() {
    check_requirements
    setup_env
    create_directories
    setup_scraper
    setup_dashboard
    show_next_steps
}

# Run main function
main