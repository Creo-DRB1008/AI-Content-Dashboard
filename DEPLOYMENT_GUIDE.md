# AI Dashboard Deployment Guide

This guide walks you through deploying the AI Dashboard with the new architecture using Render as a backend service.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Vercel         │    │  Render         │    │  SQL Server     │
│  (Frontend)     │───▶│  (Backend API)  │───▶│  (Database)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              ▲
                              │
┌─────────────────┐           │
│  GitHub Actions │───────────┘
│  (Data Collection)
└─────────────────┘
```

## Step 1: Deploy Backend to Render

### 1.1 Create Render Account
- Go to [render.com](https://render.com) and sign up
- Connect your GitHub account

### 1.2 Create Web Service
1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure the service:
   - **Name**: `ai-dashboard-backend`
   - **Root Directory**: `backend-service`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Plan**: `Starter` (or higher for production)

### 1.3 Configure Environment Variables
In Render dashboard, add these environment variables:

```bash
# Database Configuration
DB_SERVER=23.29.129.76
DB_DATABASE=aicontent
DB_USERNAME=dhairya_mac
DB_PASSWORD=q1w2e3r4t5!

# Security
API_KEY=your-secure-random-api-key-here

# Frontend URL (replace with your Vercel URL)
FRONTEND_URL=https://your-vercel-app.vercel.app

# Optional: AI Summarization
SUMMARIZATION_ENABLED=true
SUMMARIZATION_API_KEY=your-openai-api-key
SUMMARIZATION_API_URL=https://api.openai.com/v1/chat/completions
SUMMARIZATION_MODEL=gpt-3.5-turbo
SUMMARIZATION_MAX_TOKENS=150

# Server Configuration
NODE_ENV=production
PORT=3000
LOG_LEVEL=info
```

### 1.4 Deploy
- Click "Create Web Service"
- Wait for deployment to complete
- Note your Render service URL: `https://your-service-name.onrender.com`

### 1.5 Get Static IP
1. In Render dashboard, go to your service
2. Go to "Settings" → "Networking"
3. Note the **Outbound IP addresses** - these are the IPs that will connect to your database
4. Whitelist these IPs in your SQL Server firewall

## Step 2: Update Vercel Frontend

### 2.1 Add Environment Variable
In your Vercel dashboard, add:
```bash
BACKEND_URL=https://your-render-service.onrender.com
```

### 2.2 Redeploy Frontend
The frontend code has been updated to call the Render backend instead of connecting directly to the database. Simply redeploy your Vercel app.

## Step 3: Update GitHub Actions

### 3.1 Add GitHub Secrets
In your GitHub repository settings → Secrets and variables → Actions, add:

```bash
BACKEND_URL=https://your-render-service.onrender.com
API_KEY=your-secure-random-api-key-here
```

### 3.2 Update Workflow
The new workflow file `.github/workflows/daily-data-collection-render.yml` has been created. You can:

1. **Option A**: Replace your existing workflow with the new one
2. **Option B**: Keep both and disable the old one

## Step 4: Test the Setup

### 4.1 Test Backend Health
```bash
curl https://your-render-service.onrender.com/api/health
```

### 4.2 Test Data Collection
```bash
curl -X POST https://your-render-service.onrender.com/api/data/collect \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json"
```

### 4.3 Test Frontend
Visit your Vercel app and verify that content loads correctly.

### 4.4 Test GitHub Actions
1. Go to your repository → Actions
2. Run the "Daily Data Collection (via Render Backend)" workflow manually
3. Check the logs to ensure it completes successfully

## Step 5: Database Security

### 5.1 Update SQL Server Firewall
1. Remove any previous IP whitelists (GitHub Actions, Vercel, etc.)
2. Add only the Render outbound IP addresses
3. This ensures only your Render backend can access the database

### 5.2 Verify Security
- Test that direct database connections from other IPs are blocked
- Ensure only the Render backend can access your database

## Benefits of This Architecture

✅ **Enhanced Security**: Only Render's static IP can access your database
✅ **Centralized Access**: All database operations go through one service
✅ **Better Monitoring**: Single point to monitor database connections
✅ **Easier Maintenance**: One place to update database logic
✅ **Scalability**: Backend can be scaled independently
✅ **Reliability**: Render provides better uptime than serverless functions for database connections

## Monitoring and Maintenance

### Health Monitoring
- **Backend Health**: `GET /api/health`
- **Detailed Health**: `GET /api/health/detailed`
- **Collection Status**: `GET /api/data/status`

### Logs
- Check Render service logs for backend issues
- Check Vercel function logs for frontend issues
- Check GitHub Actions logs for collection issues

### Troubleshooting

**Backend not responding**:
1. Check Render service status
2. Verify environment variables
3. Check service logs

**Database connection issues**:
1. Verify IP whitelist includes Render IPs
2. Check database credentials
3. Test connection from Render logs

**Frontend not loading data**:
1. Check BACKEND_URL environment variable
2. Verify backend is responding
3. Check CORS configuration

## Cost Considerations

- **Render Starter Plan**: $7/month for the backend service
- **Vercel**: Free tier should be sufficient for frontend
- **GitHub Actions**: Free tier includes 2000 minutes/month

Total estimated cost: ~$7/month (much less than managed database solutions)
