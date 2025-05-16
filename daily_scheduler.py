#!/usr/bin/env python3
"""
Daily scheduler for the AI Dashboard.
This script runs as a daemon process and schedules data collection to run daily at 1:00 AM.
It collects data from the previous day only and stores it in the database.

Usage:
    python daily_scheduler.py [--daemon]

Options:
    --daemon    Run as a daemon process in the background
"""
import os
import sys
import time
import logging
import argparse
import schedule
import datetime
import subprocess
from pathlib import Path

# Add the current directory to the path to import from src
sys.path.append('.')

# Set up logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'daily_scheduler.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('daily_scheduler')

def collect_daily_data():
    """
    Collect data from the previous day and save it to the database.
    """
    try:
        logger.info("Starting daily data collection...")
        
        # Calculate yesterday's date
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        
        logger.info(f"Collecting data for date: {yesterday_str}")
        
        # Run the data collection script with days_ago=1 to get only yesterday's data
        cmd = [sys.executable, 'collect_and_save_data.py', '--days-ago', '1']
        
        # Execute the command
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        logger.info(f"Data collection completed successfully: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running data collection: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in data collection: {str(e)}")
        return False

def run_scheduler():
    """
    Run the scheduler to collect data daily at 1:00 AM.
    """
    logger.info("Starting scheduler...")
    
    # Schedule the data collection to run daily at 1:00 AM
    schedule.every().day.at("01:00").do(collect_daily_data)
    
    logger.info("Scheduler started. Data collection will run daily at 1:00 AM.")
    
    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def daemonize():
    """
    Daemonize the process to run in the background.
    """
    # First fork
    try:
        pid = os.fork()
        if pid > 0:
            # Exit first parent
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #1 failed: {e}")
        sys.exit(1)
    
    # Decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)
    
    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            # Exit from second parent
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #2 failed: {e}")
        sys.exit(1)
    
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    
    with open(log_file, 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())
    
    logger.info(f"Daemon started with PID {os.getpid()}")

def main():
    """
    Main entry point for the scheduler.
    """
    parser = argparse.ArgumentParser(description='Daily scheduler for AI Dashboard data collection')
    parser.add_argument('--daemon', action='store_true', help='Run as a daemon process')
    parser.add_argument('--run-now', action='store_true', help='Run data collection immediately')
    args = parser.parse_args()
    
    if args.daemon:
        logger.info("Starting in daemon mode...")
        daemonize()
    
    if args.run_now:
        logger.info("Running data collection immediately...")
        collect_daily_data()
    
    run_scheduler()

if __name__ == "__main__":
    main()
