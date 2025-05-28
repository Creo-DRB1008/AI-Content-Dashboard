# Deployment Architecture

This document outlines the current deployment architecture for the AI Content Dashboard, emphasizing the separation between the frontend dashboard and data collection processes.

## Architecture Overview

The AI Content Dashboard follows a **decoupled architecture** where:

1. **Frontend Dashboard** (Vercel) - Serves the user interface and reads data
2. **Data Collection** (GitHub Actions) - Handles all data gathering and processing
3. **Database** (SQL Server) - Centralized data storage

## Components

### 1. Frontend Dashboard (Vercel)

**Purpose**: Serve the user interface and provide read-only access to collected data.

**Deployment**: Vercel (serverless, stateless)

**Responsibilities**:
- Serve the React-based dashboard
- Provide API endpoints for reading data (`/api/content`, `/api/dates`)
- Handle user interactions (filtering, searching, date selection)

**What it does NOT do**:
- ❌ Collect data from RSS feeds
- ❌ Trigger data collection processes
- ❌ Run scheduled tasks
- ❌ Maintain long-running processes

### 2. Data Collection (GitHub Actions)

**Purpose**: Automated data collection and processing on a schedule.

**Deployment**: GitHub Actions workflow

**Schedule**: Daily at 1:00 AM UTC

**Responsibilities**:
- Collect data from RSS feeds
- Process and summarize content
- Store data in the database
- Maintain collection logs and status

**Workflow File**: `.github/workflows/daily-data-collection.yml`

### 3. Database (SQL Server)

**Purpose**: Centralized data storage for all collected content.

**Access Patterns**:
- **Write**: Only from GitHub Actions workflow
- **Read**: From Vercel dashboard API routes

## Data Flow

```
RSS Feeds → GitHub Actions → Database → Vercel Dashboard → User
```

1. **Collection**: GitHub Actions runs daily, fetches RSS data
2. **Processing**: Summarizes and processes the content
3. **Storage**: Saves processed data to SQL Server database
4. **Display**: Vercel dashboard reads from database and displays to users

## Benefits of This Architecture

### Reliability
- GitHub Actions provides consistent execution
- No dependency on Vercel's stateless environment for scheduling
- Built-in retry mechanisms and error handling

### Scalability
- Vercel handles frontend scaling automatically
- Database can be scaled independently
- Collection process runs independently of user traffic

### Monitoring
- GitHub Actions provides detailed logs and status tracking
- Clear separation of concerns for debugging
- Easy to monitor collection vs. display issues separately

### Security
- Database credentials only needed in GitHub Actions
- Frontend has read-only database access
- No sensitive operations in the public-facing dashboard

## Configuration

### GitHub Actions Secrets

Required secrets for the data collection workflow:

```
DB_SERVER=your-database-server.database.windows.net
DB_DATABASE=ai_dashboard
DB_USERNAME=your-username
DB_PASSWORD=your-password
DB_DRIVER=ODBC Driver 17 for SQL Server
SUMMARIZATION_API_KEY=your-openai-api-key
```

### Vercel Environment Variables

The Vercel deployment only needs database read access (same as above secrets).

## Monitoring and Maintenance

### GitHub Actions
- Monitor workflow runs in the Actions tab
- Check logs for collection errors
- Manually trigger runs if needed

### Vercel Dashboard
- Monitor deployment status
- Check function logs for API errors
- Monitor performance metrics

### Database
- Monitor storage usage
- Check query performance
- Maintain data retention policies

## Troubleshooting

### Data Not Updating
1. Check GitHub Actions workflow status
2. Review workflow logs for errors
3. Verify database connectivity from Actions
4. Check if secrets are properly configured

### Dashboard Not Loading Data
1. Check Vercel function logs
2. Verify database connectivity from Vercel
3. Test API endpoints directly
4. Check if data exists in database

### Collection Failures
1. Review GitHub Actions logs
2. Check RSS feed availability
3. Verify API key validity
4. Test collection script locally

## Migration Notes

### From Local Scheduler (Deprecated)

The previous architecture used local scheduling scripts:
- `backend/services/daily_scheduler.py` (DEPRECATED)
- `scripts/start_scheduler.sh` (DEPRECATED)

These are no longer used because:
- Vercel doesn't support long-running processes
- GitHub Actions provides better reliability
- Local scheduling conflicts with the new architecture

### Testing

For local development and testing:
- Use `scripts/test_daily_collection.sh` to test collection locally
- This script runs the same process as GitHub Actions
- Only for development - production uses GitHub Actions exclusively

## Future Enhancements

### Potential Improvements
- Add webhook triggers for real-time updates
- Implement incremental data collection
- Add data validation and quality checks
- Expand to additional data sources

### Scaling Considerations
- Database connection pooling
- Caching layer for frequently accessed data
- CDN for static assets
- Multiple collection workflows for different sources
