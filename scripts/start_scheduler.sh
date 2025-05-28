#!/bin/bash
# DEPRECATED: Script to start the daily scheduler as a daemon process
#
# ⚠️  WARNING: This script is DEPRECATED and should NOT be used in production.
# ⚠️  Data collection is now handled exclusively by GitHub Actions workflow.
# ⚠️  Using this script may interfere with the scheduled GitHub Actions.
#
# CURRENT APPROACH: Data collection is handled by .github/workflows/daily-data-collection.yml

echo "⚠️  WARNING: This script is DEPRECATED!"
echo "⚠️  Data collection should be handled by GitHub Actions workflow only."
echo "⚠️  Using this script may interfere with the GitHub Actions schedule."
echo "⚠️  Please use the GitHub Actions workflow: .github/workflows/daily-data-collection.yml"
echo ""

read -p "Are you sure you want to continue? This is not recommended for production. (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Exiting. Please use GitHub Actions for data collection."
    exit 1
fi

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
