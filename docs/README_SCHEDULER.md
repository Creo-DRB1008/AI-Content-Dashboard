# Data Collection Scheduling for AI Dashboard

⚠️ **IMPORTANT UPDATE**: The local scheduler described in this document is **DEPRECATED**.

## Current Approach (Recommended)

**Data collection is now handled exclusively by GitHub Actions workflow.**

- **File**: `.github/workflows/daily-data-collection.yml`
- **Schedule**: Runs daily at 1:00 AM UTC
- **Trigger**: Automatic via GitHub's cron scheduler
- **Benefits**:
  - More reliable than local scheduling
  - Better monitoring and logging via GitHub Actions interface
  - No conflicts with Vercel's stateless deployment
  - Centralized in the repository
  - No need for long-running processes

### Monitoring GitHub Actions

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. View workflow runs and logs
4. Manually trigger runs using "workflow_dispatch" if needed

### Setting up GitHub Secrets

The workflow requires these secrets to be set in your GitHub repository:

**Database Configuration:**
- `DB_SERVER` - Your database server address
- `DB_DATABASE` - Database name
- `DB_USERNAME` - Database username
- `DB_PASSWORD` - Database password
- `DB_DRIVER` - Database driver (e.g., "ODBC Driver 17 for SQL Server")

**API Keys (optional, for future use):**
- `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET`
- `LINKEDIN_API_KEY`
- `SUMMARIZATION_API_KEY` - For AI summarization service

## Legacy Local Scheduler (DEPRECATED)

⚠️ **WARNING**: The components described below are deprecated and should not be used in production.

The legacy local scheduler consisted of the following components:

1. **daily_scheduler.py**: The main scheduler script that runs as a daemon process and schedules data collection to run daily at 1:00 AM.
2. **start_scheduler.sh**: A shell script to start the scheduler as a daemon process.
3. **test_daily_collection.sh**: A shell script to test the daily data collection without waiting for the scheduled time.
4. **collect_and_save_data.py**: The script that collects data from various sources and saves it to the database.

## Setup

### Prerequisites

- Python 3.6 or higher
- Python virtual environment (recommended)
- Required Python packages (installed in the virtual environment)

### Installation

1. Make sure all the required Python packages are installed:
   ```
   pip install schedule
   ```

2. Make the shell scripts executable:
   ```
   chmod +x start_scheduler.sh
   chmod +x test_daily_collection.sh
   ```

## Usage

### Starting the Scheduler

To start the scheduler as a daemon process that runs in the background:

```bash
./start_scheduler.sh
```

This will start the scheduler, which will run the data collection process daily at 1:00 AM.

### Testing the Data Collection

To test the data collection process without waiting for the scheduled time:

```bash
./test_daily_collection.sh
```

This will run the data collection process immediately, collecting data from the past day.

### Checking if the Scheduler is Running

To check if the scheduler is running:

```bash
ps aux | grep daily_scheduler.py
```

### Stopping the Scheduler

To stop the scheduler:

```bash
pkill -f daily_scheduler.py
```

## Configuration

### Changing the Schedule

To change the time when the data collection runs, edit the `daily_scheduler.py` file and modify the following line:

```python
schedule.every().day.at("01:00").do(collect_daily_data)
```

Replace `"01:00"` with the desired time in 24-hour format (e.g., `"13:30"` for 1:30 PM).

### Changing the Data Collection Parameters

To change the parameters for data collection (e.g., number of days to collect, maximum results per source), edit the `daily_scheduler.py` file and modify the following line:

```python
cmd = [sys.executable, 'collect_and_save_data.py', '--days-ago', '1']
```

You can add additional parameters like `--max-results` followed by the desired number.

## Logs

The scheduler logs its activity to the `logs/daily_scheduler.log` file. You can check this file to see what the scheduler is doing and if there are any errors.

```bash
tail -f logs/daily_scheduler.log
```

## Troubleshooting

### Scheduler Not Starting

If the scheduler doesn't start, check the logs for errors:

```bash
cat logs/daily_scheduler.log
```

### Data Not Being Collected

If data is not being collected, you can:

1. Check the logs for errors.
2. Run the test script to see if data collection works manually.
3. Make sure the database is properly configured and accessible.

## Setting Up as a System Service

For a more robust setup, you can configure the scheduler to run as a system service using systemd (Linux) or launchd (macOS). This ensures that the scheduler starts automatically when the system boots.

### macOS (launchd)

1. Create a plist file in `~/Library/LaunchAgents/com.aidashboard.scheduler.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aidashboard.scheduler</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/AI Dashboard/start_scheduler.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/path/to/AI Dashboard/logs/scheduler_error.log</string>
    <key>StandardOutPath</key>
    <string>/path/to/AI Dashboard/logs/scheduler_output.log</string>
</dict>
</plist>
```

2. Load the service:

```bash
launchctl load ~/Library/LaunchAgents/com.aidashboard.scheduler.plist
```

3. Start the service:

```bash
launchctl start com.aidashboard.scheduler
```

Replace `/path/to/AI Dashboard/` with the actual path to your AI Dashboard directory.
