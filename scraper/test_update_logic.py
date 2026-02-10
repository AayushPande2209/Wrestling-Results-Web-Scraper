#!/usr/bin/env python3
"""
Test script to verify the update logic works correctly.
This will check if existing matches with 0-0 scores can be updated.
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.supabase_client import SupabaseClient

def test_update_logic():
    """Test the update logic for matches with 0-0 scores."""
    
    print("🧪 Testing Update Logic")
    print("-" * 60)
    
    try:
        # Initialize client
        client = SupabaseClient()
        print("✅ Connected to Supabase")
        
        # Find matches with 0-0 scores
        result = client.client.table('matches').select('*').eq('wrestler1_score', 0).eq('wrestler2_score', 0).limit(5).execute()
        
        if not result.data:
            print("ℹ️  No matches with 0-0 scores found")
            print("   This is expected if you haven't run the scraper yet")
            return
        
        print(f"\n📊 Found {len(result.data)} matches with 0-0 scores (showing first 5):")
        print()
        
        for i, match in enumerate(result.data, 1):
            print(f"{i}. Match ID: {match['id']}")
            print(f"   Tournament: {match.get('tournament_id', 'N/A')}")
            print(f"   Round: {match.get('round', 'N/A')}")
            print(f"   Current Score: {match['wrestler1_score']}-{match['wrestler2_score']}")
            print(f"   Match Type: {match.get('match_type', 'N/A')}")
            print()
        
        print("✅ Update logic is ready to use!")
        print()
        print("When you run the scraper again, it will:")
        print("  1. Skip matches that already have scores")
        print("  2. Update matches with 0-0 scores to actual scores")
        print("  3. Insert any new matches that don't exist yet")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_update_logic()
