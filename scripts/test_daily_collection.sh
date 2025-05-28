#!/bin/bash
# Script to test the daily data collection locally (for development/testing only)
#
# NOTE: This script is for LOCAL TESTING ONLY. In production, data collection
# is handled by GitHub Actions workflow (.github/workflows/daily-data-collection.yml).
#
# This script runs the same collection process that GitHub Actions uses,
# but locally for development and testing purposes.

echo "🧪 Running LOCAL data collection test..."
echo "📝 Note: In production, this runs automatically via GitHub Actions"
echo ""

# Change to the project directory
cd "$(dirname "$0")"

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if Python virtual environment exists
if [ -d "venv" ]; then
    echo "Using Python virtual environment..."
    source venv/bin/activate
fi

# Run the data collection for the past 1 day (same as GitHub Actions)
echo "Running data collection for the past 1 day..."
python backend/services/collect_and_save_data.py --days-ago 1 --max-results 20

# Check if the collection was successful
if [ $? -eq 0 ]; then
    echo "Data collection completed successfully."
else
    echo "Data collection failed. Check logs for errors."
    exit 1
fi
