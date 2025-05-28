# Deploying the AI Dashboard on Vercel

This guide provides step-by-step instructions for deploying the AI Dashboard on Vercel.

## Prerequisites

1. A GitHub account
2. A Vercel account (you can sign up at https://vercel.com using your GitHub account)
3. Your project pushed to GitHub (which you've already done)

## Deployment Steps

### 1. Sign in to Vercel

Go to https://vercel.com and sign in with your GitHub account.

### 2. Import Your Repository

1. Click on "Add New..." and select "Project"
2. Connect your GitHub account if you haven't already
3. Find and select your repository "AI-Content-Dashboard"
4. Click "Import"

### 3. Configure Project Settings

On the configuration page:

1. **Framework Preset**: Vercel should automatically detect Next.js
2. **Root Directory**: Leave as default (/)
3. **Build Command**: Leave as default (next build)
4. **Output Directory**: Leave as default (.next)
5. **Environment Variables**: Add the following environment variables:
   - `TWITTER_API_KEY`: Your Twitter API key
   - `TWITTER_API_SECRET`: Your Twitter API secret
   - `TWITTER_ACCESS_TOKEN`: Your Twitter access token
   - `TWITTER_ACCESS_SECRET`: Your Twitter access secret
   - `LINKEDIN_API_KEY`: Your LinkedIn API key
   - `DATABASE_URL`: Your database connection string (for production, consider using a hosted database service)

6. Click "Deploy"

### 4. Wait for Deployment

Vercel will now build and deploy your application. This may take a few minutes.

### 5. Access Your Deployed Application

Once the deployment is complete, Vercel will provide you with a URL to access your application (e.g., https://ai-content-dashboard.vercel.app).

## Setting Up Automatic Deployments

By default, Vercel will automatically deploy your application whenever you push changes to the main branch of your GitHub repository. This means:

1. Make changes to your code locally
2. Commit the changes to Git
3. Push to GitHub
4. Vercel will automatically deploy the new version

## Custom Domains

If you want to use a custom domain for your dashboard:

1. Go to your project on Vercel
2. Click on "Settings" > "Domains"
3. Add your domain and follow the instructions to configure DNS settings

## Troubleshooting

### Build Failures

If your build fails, check the build logs for errors. Common issues include:

- Missing dependencies
- Environment variables not set correctly
- Syntax errors in your code

### Database Connection Issues

If your application can't connect to the database:

- Ensure your DATABASE_URL environment variable is correct
- Make sure your database is accessible from Vercel's servers (public or with proper network configuration)
- Consider using a database service that provides a connection string compatible with Vercel's serverless environment

### API Rate Limiting

If you're experiencing issues with API rate limiting:

- Check your Twitter and LinkedIn API usage
- Consider implementing caching strategies
- Adjust your data collection frequency

## GitHub Actions for Data Collection

The GitHub Action for daily data collection is already set up in your repository. It will run at 1:00 AM UTC every day to collect data from various sources.

To monitor the GitHub Action:

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. You'll see the workflow runs listed there

If you need to make changes to the GitHub Action, edit the `.github/workflows/daily-data-collection.yml` file.
