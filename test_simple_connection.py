#!/usr/bin/env python3
"""
Simple SQL Server connection test
"""
import pyodbc
import sys

def test_direct_connection():
    """Test direct pyodbc connection."""
    
    # Try different connection approaches
    connection_strings = [
        # Approach 1: Direct connection with TDS 7.3
        (
            "DRIVER={FreeTDS};"
            "SERVER=23.29.129.76;"
            "PORT=1433;"
            "DATABASE=aicontent;"
            "UID=dhairya_mac;"
            "PWD=q1w2e3r4t5!;"
            "TDS_Version=7.3;"
        ),
        # Approach 2: Direct connection with TDS 8.0
        (
            "DRIVER={FreeTDS};"
            "SERVER=23.29.129.76;"
            "PORT=1433;"
            "DATABASE=aicontent;"
            "UID=dhairya_mac;"
            "PWD=q1w2e3r4t5!;"
            "TDS_Version=8.0;"
        ),
        # Approach 3: Without explicit TDS version
        (
            "DRIVER={FreeTDS};"
            "SERVER=23.29.129.76;"
            "PORT=1433;"
            "DATABASE=aicontent;"
            "UID=dhairya_mac;"
            "PWD=q1w2e3r4t5!;"
        ),
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        try:
            print(f"Testing connection approach {i}...")
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()
            print(f"✅ Connection successful with approach {i}!")
            print(f"Server version: {version[0]}")
            
            cursor.execute("SELECT DB_NAME()")
            db_name = cursor.fetchone()
            print(f"Current database: {db_name[0]}")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Approach {i} failed: {e}")
            continue
    
    return False

if __name__ == "__main__":
    success = test_direct_connection()
    sys.exit(0 if success else 1) 