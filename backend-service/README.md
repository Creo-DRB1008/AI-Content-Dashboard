# AI Dashboard Backend Service

This backend service acts as the single point of database access for the AI Dashboard project. It provides API endpoints for the Vercel frontend and handles data collection triggered by GitHub Actions.

## Architecture

```
Vercel Frontend → Render Backend → SQL Server Database
GitHub Actions → Render Backend → SQL Server Database
```

## Features

- **Read API**: Provides content and date endpoints for the frontend
- **Data Collection**: RSS feed collection and AI summarization
- **Security**: API key authentication for data collection
- **Health Monitoring**: Health check endpoints
- **Logging**: Comprehensive logging with Winston
- **Rate Limiting**: Protection against abuse

## API Endpoints

### Public Endpoints (for Vercel Frontend)

- `GET /` - Service information
- `GET /api/health` - Health check
- `GET /api/content` - Get content with optional filters
- `GET /api/content/dates` - Get available dates
- `GET /api/content/stats` - Get content statistics

### Protected Endpoints (for GitHub Actions)

- `POST /api/data/collect` - Trigger data collection (requires API key)
- `GET /api/data/status` - Get collection status

## Environment Variables

### Required

```bash
# Database
DB_SERVER=your-sql-server-ip
DB_DATABASE=aicontent
DB_USERNAME=your-username
DB_PASSWORD=your-password

# Security
API_KEY=your-secure-api-key

# Frontend (for CORS)
FRONTEND_URL=https://your-vercel-app.vercel.app
```

### Optional

```bash
# Summarization
SUMMARIZATION_ENABLED=true
SUMMARIZATION_API_KEY=your-openai-api-key
SUMMARIZATION_API_URL=https://api.openai.com/v1/chat/completions
SUMMARIZATION_MODEL=gpt-3.5-turbo
SUMMARIZATION_MAX_TOKENS=150

# Server
NODE_ENV=production
PORT=3000
LOG_LEVEL=info
```

## Deployment to Render

1. **Create a new Web Service** on Render
2. **Connect your repository** containing this backend-service folder
3. **Set the root directory** to `backend-service`
4. **Configure environment variables** in Render dashboard
5. **Deploy** - Render will automatically install dependencies and start the service

### Render Configuration

- **Build Command**: `npm install`
- **Start Command**: `npm start`
- **Environment**: Node.js
- **Plan**: Starter (or higher for production)

## Local Development

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start development server
npm run dev
```

## GitHub Actions Integration

Update your GitHub Actions workflow to call the Render backend:

```yaml
- name: Collect Data
  env:
    BACKEND_URL: https://your-render-service.onrender.com
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    curl -X POST "$BACKEND_URL/api/data/collect" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json"
```

## Vercel Frontend Integration

Update your Vercel frontend API calls to point to the Render backend:

```javascript
// In your Vercel frontend
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://your-render-service.onrender.com';

// Replace direct database calls with API calls
const response = await fetch(`${BACKEND_URL}/api/content`);
const content = await response.json();
```

## Security Features

- **API Key Authentication**: Data collection endpoints require valid API key
- **CORS Protection**: Only allows requests from configured frontend URLs
- **Rate Limiting**: Prevents abuse with request rate limits
- **Input Validation**: Validates and sanitizes all inputs
- **Error Handling**: Comprehensive error handling and logging

## Monitoring

- **Health Checks**: `/api/health` endpoint for monitoring
- **Logging**: All requests and errors are logged
- **Status Endpoint**: `/api/data/status` shows collection statistics

## Static IP Benefits

- **Database Security**: Only Render's static IP needs database access
- **Centralized Access**: All database operations go through one service
- **Easier Monitoring**: Single point to monitor database connections
- **Better Security**: Reduced attack surface compared to multiple access points
