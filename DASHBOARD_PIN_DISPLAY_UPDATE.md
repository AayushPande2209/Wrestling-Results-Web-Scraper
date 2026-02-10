# Dashboard Update: Pin Display

## Changes Made

Updated the dashboard to display pin time instead of "0-0" for pin matches.

### Files Modified

1. **dashboard/src/types/database.ts**
   - Added `match_time: string | null` field to Match interface
   - This field stores the pin time (e.g., "5:32")

2. **dashboard/src/app/wrestlers/[id]/page.tsx**
   - Updated `getMatchResult()` function to check if match is a pin
   - If pin with match_time: displays the time (e.g., "5:32")
   - If other match type: displays the score (e.g., "3-0")

3. **dashboard/src/app/tournaments/[id]/page.tsx**
   - Updated score display in matches table
   - If pin with match_time: displays the time
   - If other match type: displays the score

## How It Works

### Before:
```
Match Type: Pin
Score: 0-0
```

### After:
```
Match Type: Pin
Score: 5:32  (shows the pin time)
```

### For Other Match Types:
```
Match Type: Decision
Score: 3-0  (shows the actual score)
```

## Display Logic

```typescript
// Wrestler detail page
if (match.match_type === 'pin' && match.match_time) {
  return { result, score: match.match_time }  // Show "5:32"
} else {
  return { result, score: `${score1}-${score2}` }  // Show "3-0"
}

// Tournament page
{match.match_type === 'pin' && match.match_time 
  ? match.match_time           // Show "5:32"
  : `${score1} - ${score2}`    // Show "3 - 0"
}
```

## Testing

To see the changes:

1. **Start the dashboard:**
   ```bash
   cd dashboard
   npm run dev
   ```

2. **View wrestler profiles:**
   - Go to http://localhost:3000/wrestlers
   - Click on any wrestler
   - Look at their match history
   - Pin matches will show the time instead of 0-0

3. **View tournament details:**
   - Go to http://localhost:3000/tournaments
   - Click on any tournament
   - Look at the match results table
   - Pin matches will show the time in the Score column

## Example Display

### Wrestler Match History Table:
```
Result | Opponent      | Score | Match Type | Tournament
W      | John Smith    | 5:32  | Pin        | State Finals
L      | Mike Jones    | 0-3   | Decision   | Regionals
W      | Tom Brown     | 1:45  | Pin        | Districts
W      | Dave Wilson   | 15-0  | Tech Fall  | Sectionals
```

### Tournament Results Table:
```
Wrestler 1    | Wrestler 2    | Score | Winner       | Match Type
Aarush M.     | Mark A.       | 5:32  | Mark A.      | PIN
Aarush M.     | John S.       | 3-0   | Aarush M.    | DECISION
Blake A.      | Tom B.        | 1:27  | Blake A.     | PIN
```

## Benefits

1. **More Informative:** Shows when the pin happened instead of meaningless 0-0
2. **Accurate:** Reflects the actual data available from DubStat
3. **Consistent:** Pin time is the standard way to display pin results in wrestling
4. **User-Friendly:** Users immediately understand "5:32" means pinned at 5 minutes 32 seconds

## Notes

- Pin times are stored in the database as strings (e.g., "5:32", "1:45")
- If a pin doesn't have a time (rare), it will fall back to showing 0-0
- All other match types (Decision, Tech Fall, Major Decision) continue to show scores normally
- This change is purely cosmetic - no database changes required

## Deployment

The changes are ready to deploy. Just rebuild and restart the dashboard:

```bash
cd dashboard
npm run build
npm start
```

Or if using Vercel, just push to your repository and it will auto-deploy.
