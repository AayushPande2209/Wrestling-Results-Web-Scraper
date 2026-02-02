# Setting Up Environment Variables

## Quick Setup Guide

### Step 1: Get Your Supabase Credentials

1. **Go to your Supabase Dashboard**
   - Visit: https://supabase.com/dashboard
   - Log in to your account

2. **Select Your Project**
   - Click on your project (or create a new one if you don't have one)

3. **Get Your API Keys**
   - Click on **Settings** (gear icon in the left sidebar)
   - Click on **API** in the settings menu
   - You'll see:
     - **Project URL**: Something like `https://xxxxx.supabase.co`
     - **anon public** key: A long string starting with `eyJ...`
     - **service_role** key: Another long string (keep this secret!)

### Step 2: Update Your .env File

1. **Open the `.env` file** in the root of your project
   - Location: `/Users/aayush/Desktop/Coding/API Projects/Wrestling_Scraper/.env`

2. **Replace the placeholder values:**
   ```bash
   SUPABASE_URL=https://qsncbvjopbennwsxxkyi.supabase.co
   SUPABASE_ANON_KEY=paste-your-anon-key-here
   ```

3. **For write operations (scraper), you may need the service_role key:**
   - The scraper needs to INSERT data into the database
   - If the anon key doesn't have write permissions, use the service_role key
   - **Important**: Never commit the service_role key to git!

### Step 3: Test Your Configuration

Run the test script to verify your credentials work:

```bash
cd scraper
python test_database_insert.py
```

If you see "✅ Test passed! Data is being inserted into the database", you're all set!

## Troubleshooting

### Error: "Invalid API key"
- Double-check that you copied the entire key (they're very long)
- Make sure there are no extra spaces or line breaks
- Verify you're using the correct key (anon vs service_role)

### Error: "Permission denied" or "401 Unauthorized"
- The anon key might not have write permissions
- Try using the service_role key instead
- Check your Supabase RLS (Row Level Security) policies

### Can't find the .env file?
- Make sure you're in the project root directory
- The file should be at: `Wrestling_Scraper/.env`
- If it doesn't exist, create it with the template above

## Security Notes

⚠️ **Important Security Tips:**
- Never commit your `.env` file to git
- The `.env` file should already be in `.gitignore`
- Never share your service_role key publicly
- The anon key is safe to use in frontend code, but service_role key should only be used server-side
