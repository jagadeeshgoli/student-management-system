# config/db.py
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'database': 'student_management_db',
    'user': 'jai',
    'password': '23',      
    'port': 5432
}

def get_connection():
    """
    Returns a new database connection with RealDictCursor for named access.
    Usage:
        conn = get_connection()
        cursor = conn.cursor()
        # ... your queries ...
        conn.close()  # Don't forget to close!
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def test_connection():
    """Test if database connection works"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Database connected successfully!")
            print(f"PostgreSQL version: {version[0]}")
            cursor.close()
        except psycopg2.Error as e:
            print(f"Connection test failed: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    test_connection()