# GitHub Actions Data Collection Setup

This document explains how to set up and configure the GitHub Actions workflow for automated daily data collection.

## Overview

The AI Content Dashboard uses GitHub Actions to automatically collect data from RSS feeds daily at 1:00 AM UTC. This approach provides several advantages over local scheduling:

- **Reliability**: GitHub's infrastructure ensures consistent execution
- **Monitoring**: Built-in logging and status tracking
- **Stateless**: Compatible with Vercel's serverless deployment
- **Centralized**: All configuration in the repository

## Workflow File

The workflow is defined in `.github/workflows/daily-data-collection.yml` and includes:

- **Schedule**: Daily execution at 1:00 AM UTC via cron
- **Manual Trigger**: Can be run manually via `workflow_dispatch`
- **Environment Setup**: Python 3.9 with required dependencies
- **Data Collection**: Runs the collection script with proper environment variables
- **Artifact Storage**: Commits collected data back to the repository

## Required GitHub Secrets

To set up the workflow, you need to configure the following secrets in your GitHub repository:

### Database Configuration

Navigate to your GitHub repository → Settings → Secrets and variables → Actions, then add:

- `DB_SERVER` - Your database server address (e.g., `your-server.database.windows.net`)
- `DB_DATABASE` - Database name (e.g., `ai_dashboard`)
- `DB_USERNAME` - Database username
- `DB_PASSWORD` - Database password
- `DB_DRIVER` - Database driver (e.g., `ODBC Driver 17 for SQL Server`)

### API Keys (Optional)

For future expansion, you can also configure:

- `TWITTER_API_KEY` - Twitter API key
- `TWITTER_API_SECRET` - Twitter API secret
- `TWITTER_ACCESS_TOKEN` - Twitter access token
- `TWITTER_ACCESS_SECRET` - Twitter access token secret
- `LINKEDIN_API_KEY` - LinkedIn API key
- `SUMMARIZATION_API_KEY` - OpenAI or compatible API key for summarization

## Setting Up Secrets

1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret with its name and value
6. Click **Add secret**

## Monitoring the Workflow

### Viewing Workflow Runs

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. You'll see a list of workflow runs with their status
4. Click on any run to view detailed logs

### Manual Triggering

To manually trigger the data collection:

1. Go to **Actions** tab
2. Click on **Daily Data Collection** workflow
3. Click **Run workflow** button
4. Select the branch and click **Run workflow**

### Checking Logs

Each workflow run provides detailed logs:

- **Setup logs**: Python installation and dependency setup
- **Collection logs**: Data collection process output
- **Error logs**: Any errors that occurred during execution

## Troubleshooting

### Common Issues

**Workflow not running:**
- Check that the cron schedule is correct
- Verify the workflow file syntax
- Ensure the repository has Actions enabled

**Database connection errors:**
- Verify all database secrets are correctly set
- Check database server accessibility
- Ensure database credentials are valid

**Collection script errors:**
- Check the script path in the workflow
- Verify Python dependencies are correctly installed
- Review the collection script logs

### Debugging Steps

1. **Check workflow syntax**: Use GitHub's workflow validator
2. **Review secrets**: Ensure all required secrets are set
3. **Test manually**: Use the manual trigger to test immediately
4. **Check logs**: Review detailed logs for specific error messages
5. **Local testing**: Use `scripts/test_daily_collection.sh` for local debugging

## Workflow Schedule

The workflow runs daily at 1:00 AM UTC. To change the schedule:

1. Edit `.github/workflows/daily-data-collection.yml`
2. Modify the cron expression in the `schedule` section
3. Commit the changes

Example cron expressions:
- `'0 1 * * *'` - Daily at 1:00 AM UTC
- `'0 */6 * * *'` - Every 6 hours
- `'0 9 * * 1-5'` - Weekdays at 9:00 AM UTC

## Data Storage

The workflow collects data and:

1. **Saves to database**: Primary storage for the dashboard
2. **Creates JSON files**: Backup files in the `data/` directory
3. **Commits to repository**: Automatic commits with collected data

## Security Considerations

- **Secrets**: Never commit secrets to the repository
- **Database access**: Use read/write permissions only for the collection database
- **API keys**: Rotate keys regularly and monitor usage
- **Repository access**: Limit who can modify workflow files and secrets

## Next Steps

After setting up the GitHub Actions workflow:

1. **Test the workflow**: Run it manually to ensure it works
2. **Monitor initial runs**: Check logs for any issues
3. **Verify data collection**: Confirm data appears in your dashboard
4. **Set up notifications**: Configure GitHub to notify you of workflow failures
