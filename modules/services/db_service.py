import sqlite3
import bcrypt
from modules.services.logger_service import log_info, log_error
import shutil
from datetime import datetime
import os

DB_NAME = "smartselect.db"

def get_connection():
    """Helper to handle connection timeouts if database is busy."""
    return sqlite3.connect(DB_NAME, timeout=10)

def init_db():
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                region TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                type TEXT,
                content TEXT
            )
        """)
        conn.commit()
        log_info("Database initialized successfully.")
    except Exception as e:
        log_error(f"Failed to initialize database: {str(e)}")
    finally:
        conn.close()

def create_user(username, password, region):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, region))
        conn.commit()
        log_info(f"New user registered: {username} in {region}")
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        log_error(f"Error creating user {username}: {str(e)}")
        return False
    finally:
        conn.close()

def save_scan(user, scan_type, content):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "INSERT INTO scans (user, type, content) VALUES (?, ?, ?)",
            (user, scan_type, content)
        )
        conn.commit()
        log_info(f"Scan saved for user: {user}")
    except Exception as e:
        log_error(f"Failed to save scan for {user}: {str(e)}")
    finally:
        conn.close()

def get_scans(user):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, type, content FROM scans WHERE user=? ORDER BY id DESC", (user,))
        rows = c.fetchall()
        return rows
    except Exception as e:
        log_error(f"Error fetching scans for {user}: {str(e)}")
        return []
    finally:
        conn.close()

def delete_scan(scan_id):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM scans WHERE id=?", (scan_id,))
        conn.commit()
        log_info(f"Scan deleted ID: {scan_id}")
    except Exception as e:
        log_error(f"Error deleting scan {scan_id}: {str(e)}")
    finally:
        conn.close()

def transfer_guest_data(guest_id, real_username):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE scans SET user = ? WHERE user = ?", (real_username, guest_id))
        conn.commit()
        log_info(f"Data transferred from {guest_id} to {real_username}")
    except Exception as e:
        log_error(f"Transfer failed for {real_username}: {str(e)}")
    finally:
        conn.close()



def backup_database():
    """Creates a timestamped copy of the database in a backup folder."""
    BACKUP_DIR = "backups"
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"smartselect_backup_{timestamp}.db")
        
        shutil.copy2(DB_NAME, backup_path)
        log_info(f"Database backup created: {backup_path}")
    except Exception as e:
        log_error(f"Backup failed: {str(e)}")