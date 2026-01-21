# Wrestling Analytics Platform - Deployment Guide

## Vercel Deployment

This guide covers deploying the Wrestling Analytics Dashboard to Vercel.

### Prerequisites

1. **GitHub Repository**: Ensure your code is pushed to a GitHub repository
2. **Vercel Account**: Create a free account at [vercel.com](https://vercel.com)
3. **Supabase Project**: Have your Supabase project URL and anon key ready

### Step 1: Connect GitHub Repository

1. Log in to your Vercel dashboard
2. Click "New Project"
3. Import your GitHub repository containing the wrestling analytics platform
4. Select the repository and click "Import"

### Step 2: Configure Project Settings

1. **Root Directory**: Set to `dashboard` (since the Next.js app is in the dashboard folder)
2. **Framework Preset**: Vercel should auto-detect Next.js
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### Step 3: Set Up Environment Variables

In the Vercel project settings, add these environment variables:

#### Required Variables
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
NEXTAUTH_SECRET=your-secure-random-string-here
NEXTAUTH_URL=https://your-app.vercel.app
```

#### How to Get These Values

**Supabase Variables:**
1. Go to your Supabase project dashboard
2. Navigate to Settings > API
3. Copy the "Project URL" for `NEXT_PUBLIC_SUPABASE_URL`
4. Copy the "anon public" key for `NEXT_PUBLIC_SUPABASE_ANON_KEY`

**NextAuth Variables:**
1. Generate a secure random string for `NEXTAUTH_SECRET`:
   ```bash
   openssl rand -base64 32
   ```
2. Set `NEXTAUTH_URL` to your Vercel app URL (e.g., `https://wrestling-analytics.vercel.app`)

### Step 4: Deploy

1. Click "Deploy" in Vercel
2. Wait for the build to complete
3. Your app will be available at the provided Vercel URL

### Step 5: Test Production Deployment

1. Visit your deployed app URL
2. Test the wrestlers list page
3. Test individual wrestler profiles
4. Verify data loads correctly from Supabase
5. Check that all navigation works

### Troubleshooting

#### Build Failures
- Check the build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`
- Verify TypeScript compilation passes locally

#### Environment Variable Issues
- Double-check all environment variables are set correctly
- Ensure `NEXT_PUBLIC_` prefix for client-side variables
- Verify Supabase URL and keys are correct

#### Database Connection Issues
- Verify Supabase project is active
- Check RLS policies allow public read access
- Ensure database tables exist and have data

### Automatic Deployments

Once connected to GitHub:
- Every push to the main branch triggers a new deployment
- Pull requests create preview deployments
- Vercel provides deployment status in GitHub

### Custom Domain (Optional)

To use a custom domain:
1. Go to Project Settings > Domains in Vercel
2. Add your custom domain
3. Configure DNS records as instructed
4. Update `NEXTAUTH_URL` environment variable

### Performance Optimization

For production:
- Enable Vercel Analytics (optional)
- Configure caching headers if needed
- Monitor Core Web Vitals in Vercel dashboard

## Next Steps

After successful deployment:
1. Update the scraper configuration to use production database
2. Test the complete data pipeline
3. Document the production URLs for team access