# Testing the AI Dashboard Data Collection

This document provides instructions for testing the data collection components of the AI Dashboard project.

## Prerequisites

1. Python 3.8+ installed
2. Virtual environment activated
3. Dependencies installed:
   ```
   pip install -r requirements.txt
   ```
4. `.env` file created with appropriate API keys (see `.env.example`)

## Test Scripts

The project includes several test scripts to verify different components:

### 1. Test Individual Collectors

Run the following command to test the individual data collectors:

```bash
python test_collectors.py
```

This script tests:
- RSS feed collector
- LinkedIn data collector (simulated data)
- Twitter collector (structure only, will fail with placeholder API keys)
- Main collector that combines all sources

### 2. Test Database Models

Run the following command to test the database models and storage:

```bash
python test_database.py
```

This script tests:
- Database connection
- Category model
- Content model
- Storage module

### 3. Test Full Pipeline

Run the following command to test the entire data collection pipeline:

```bash
python test_pipeline.py
```

This script tests the full data collection and storage pipeline:
1. Initialize the database
2. Collect data from all sources
3. Save data to JSON
4. Save data to database
5. Retrieve data from database

## Expected Results

### With Placeholder API Keys

When running with placeholder API keys (as in the provided `.env` file):

- RSS collector should work correctly and fetch real data
- LinkedIn collector will use simulated data
- Twitter collector will fail with authentication errors
- Database tests should pass using SQLite

### With Valid API Keys

When configured with valid API keys:

- All collectors should work correctly
- All tests should pass

## Troubleshooting

### Common Issues

1. **Module Import Errors**:
   - Make sure you're running the scripts from the project root directory
   - Check that the virtual environment is activated

2. **API Authentication Errors**:
   - Verify that your `.env` file contains valid API keys
   - For testing purposes, you can use the simulated data options

3. **Database Connection Errors**:
   - The test scripts use SQLite for testing, which doesn't require a PostgreSQL server
   - For production, make sure PostgreSQL is installed and running

### Logs

Check the `logs` directory for detailed logs from each component:

- `main_*.log`: Main application logs
- `twitter_collector_*.log`: Twitter collector logs
- `linkedin_collector_*.log`: LinkedIn collector logs
- `rss_collector_*.log`: RSS collector logs
- `database_*.log`: Database operation logs

## Next Steps

After verifying that the data collection components are working:

1. Configure real API keys for Twitter and LinkedIn
2. Set up a PostgreSQL database for production
3. Implement the data processing pipeline (Phase 2)
4. Develop the backend API (Phase 3)
5. Create the frontend (Phase 4)
