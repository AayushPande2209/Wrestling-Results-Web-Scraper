#!/usr/bin/env python3
"""
Manual script to update pin scores if you have the score data from another source.
Since DubStat doesn't provide scores for pins, this allows manual updates.

Usage:
    python3 update_pin_scores.py
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.supabase_client import SupabaseClient


def list_pin_matches_with_zero_scores():
    """List all pin matches that have 0-0 scores."""
    client = SupabaseClient()
    
    print("🔍 Finding pin matches with 0-0 scores...")
    print("-" * 80)
    
    # Get all pin matches with 0-0 scores
    result = client.client.table('matches').select('''
        id,
        wrestler1_id,
        wrestler2_id,
        tournament_id,
        round,
        wrestler1_score,
        wrestler2_score,
        match_type,
        match_time,
        wrestler1:wrestler1_id(name),
        wrestler2:wrestler2_id(name),
        tournament:tournament_id(name)
    ''').eq('match_type', 'pin').eq('wrestler1_score', 0).eq('wrestler2_score', 0).execute()
    
    if not result.data:
        print("✅ No pin matches with 0-0 scores found!")
        return []
    
    print(f"📊 Found {len(result.data)} pin matches with 0-0 scores:\n")
    
    matches = []
    for i, match in enumerate(result.data, 1):
        wrestler1_name = match['wrestler1']['name'] if match.get('wrestler1') else 'Unknown'
        wrestler2_name = match['wrestler2']['name'] if match.get('wrestler2') else 'Unknown'
        tournament_name = match['tournament']['name'] if match.get('tournament') else 'Unknown'
        
        print(f"{i}. Match ID: {match['id']}")
        print(f"   Wrestlers: {wrestler1_name} vs {wrestler2_name}")
        print(f"   Tournament: {tournament_name}")
        print(f"   Round: {match.get('round', 'N/A')}")
        print(f"   Match Time: {match.get('match_time', 'N/A')}")
        print(f"   Current Score: {match['wrestler1_score']}-{match['wrestler2_score']}")
        print()
        
        matches.append({
            'id': match['id'],
            'wrestler1': wrestler1_name,
            'wrestler2': wrestler2_name,
            'tournament': tournament_name,
            'round': match.get('round'),
            'match_time': match.get('match_time')
        })
    
    return matches


def update_match_score(match_id: str, wrestler1_score: int, wrestler2_score: int):
    """Update a specific match's score."""
    client = SupabaseClient()
    
    try:
        result = client.client.table('matches').update({
            'wrestler1_score': wrestler1_score,
            'wrestler2_score': wrestler2_score
        }).eq('id', match_id).execute()
        
        if result.data:
            print(f"✅ Updated match {match_id} to {wrestler1_score}-{wrestler2_score}")
            return True
        else:
            print(f"❌ Failed to update match {match_id}")
            return False
    except Exception as e:
        print(f"❌ Error updating match {match_id}: {e}")
        return False


def interactive_update():
    """Interactive mode to update pin scores."""
    print("🏆 Pin Score Manual Update Tool")
    print("=" * 80)
    print()
    
    matches = list_pin_matches_with_zero_scores()
    
    if not matches:
        return
    
    print("-" * 80)
    print("\n📝 Update Instructions:")
    print("   - Enter the match number to update")
    print("   - Enter 'q' to quit")
    print("   - Enter 'list' to see the list again")
    print()
    
    while True:
        choice = input("Enter match number to update (or 'q' to quit, 'list' to see list): ").strip()
        
        if choice.lower() == 'q':
            print("👋 Goodbye!")
            break
        
        if choice.lower() == 'list':
            print()
            list_pin_matches_with_zero_scores()
            continue
        
        try:
            match_num = int(choice)
            if match_num < 1 or match_num > len(matches):
                print(f"❌ Invalid match number. Please enter 1-{len(matches)}")
                continue
            
            match = matches[match_num - 1]
            print(f"\n📝 Updating: {match['wrestler1']} vs {match['wrestler2']}")
            print(f"   Tournament: {match['tournament']}")
            print(f"   Round: {match['round']}")
            print(f"   Match Time: {match['match_time']}")
            print()
            
            wrestler1_score = input(f"   Enter score for {match['wrestler1']}: ").strip()
            wrestler2_score = input(f"   Enter score for {match['wrestler2']}: ").strip()
            
            try:
                w1_score = int(wrestler1_score)
                w2_score = int(wrestler2_score)
                
                confirm = input(f"\n   Update to {w1_score}-{w2_score}? (y/n): ").strip().lower()
                if confirm == 'y':
                    if update_match_score(match['id'], w1_score, w2_score):
                        print("   ✅ Score updated successfully!\n")
                    else:
                        print("   ❌ Failed to update score\n")
                else:
                    print("   ⏭️  Skipped\n")
            except ValueError:
                print("   ❌ Invalid scores. Please enter numbers.\n")
        
        except ValueError:
            print(f"❌ Invalid input. Please enter a number 1-{len(matches)}, 'list', or 'q'\n")


def bulk_update_from_csv():
    """Update multiple matches from a CSV file."""
    print("📄 Bulk Update from CSV")
    print("-" * 80)
    print()
    print("CSV Format: match_id,wrestler1_score,wrestler2_score")
    print("Example: abc123,15,7")
    print()
    
    csv_file = input("Enter CSV file path (or 'q' to cancel): ").strip()
    
    if csv_file.lower() == 'q':
        return
    
    try:
        import csv
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            updated = 0
            failed = 0
            
            for row in reader:
                match_id = row['match_id']
                w1_score = int(row['wrestler1_score'])
                w2_score = int(row['wrestler2_score'])
                
                if update_match_score(match_id, w1_score, w2_score):
                    updated += 1
                else:
                    failed += 1
            
            print()
            print(f"✅ Updated: {updated}")
            print(f"❌ Failed: {failed}")
    
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function."""
    print()
    print("Choose update mode:")
    print("1. Interactive (update one at a time)")
    print("2. Bulk from CSV")
    print("3. Just list matches")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == '1':
        interactive_update()
    elif choice == '2':
        bulk_update_from_csv()
    elif choice == '3':
        list_pin_matches_with_zero_scores()
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
