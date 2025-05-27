#!/bin/bash
# Script to start the daily scheduler as a daemon process

# Change to the project directory
cd "$(dirname "$0")"

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if Python virtual environment exists
if [ -d "venv" ]; then
    echo "Using Python virtual environment..."
    source venv/bin/activate
fi

# Start the scheduler as a daemon
echo "Starting daily scheduler..."
python daily_scheduler.py --daemon

# Check if the scheduler started successfully
if [ $? -eq 0 ]; then
    echo "Scheduler started successfully. Check logs/daily_scheduler.log for details."
else
    echo "Failed to start scheduler. Check logs/daily_scheduler.log for errors."
    exit 1
fi

echo "To check if the scheduler is running, use: ps aux | grep daily_scheduler.py"
echo "To stop the scheduler, use: pkill -f daily_scheduler.py"
