import sqlite3
import os
from datetime import datetime
import secrets
from typing import Dict, List, Optional, Tuple
import json

# Database path
DB_PATH = "location_services.db"

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create tracking_sessions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tracking_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create location_points table
    c.execute('''
        CREATE TABLE IF NOT EXISTS location_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            accuracy REAL,
            FOREIGN KEY (session_id) REFERENCES tracking_sessions (id)
        )
    ''')
    
    # Create groups table
    c.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Create group_members table
    c.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            user_id INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            permissions TEXT DEFAULT 'viewer',
            FOREIGN KEY (group_id) REFERENCES groups (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create game_sessions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER DEFAULT 0,
            rounds_completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_session_token() -> str:
    """Generate a secure random session token."""
    return secrets.token_urlsafe(32)

def create_tracking_session(user_id: int) -> str:
    """Create a new tracking session and return the session token."""
    session_token = generate_session_token()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO tracking_sessions (user_id, session_token)
        VALUES (?, ?)
    ''', (user_id, session_token))
    
    conn.commit()
    conn.close()
    return session_token

def add_location_point(session_token: str, lat: float, lon: float, accuracy: float) -> bool:
    """Add a new location point to an active tracking session."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get session ID
    c.execute('SELECT id FROM tracking_sessions WHERE session_token = ? AND is_active = TRUE', 
              (session_token,))
    result = c.fetchone()
    
    if result:
        session_id = result[0]
        c.execute('''
            INSERT INTO location_points (session_id, latitude, longitude, accuracy)
            VALUES (?, ?, ?, ?)
        ''', (session_id, lat, lon, accuracy))
        
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

def get_location_history(session_token: str) -> List[Dict]:
    """Get location history for a tracking session."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT lp.latitude, lp.longitude, lp.timestamp, lp.accuracy
        FROM location_points lp
        JOIN tracking_sessions ts ON lp.session_id = ts.id
        WHERE ts.session_token = ?
        ORDER BY lp.timestamp ASC
    ''', (session_token,))
    
    results = c.fetchall()
    conn.close()
    
    return [
        {
            'latitude': lat,
            'longitude': lon,
            'timestamp': timestamp,
            'accuracy': accuracy
        }
        for lat, lon, timestamp, accuracy in results
    ]

def end_tracking_session(session_token: str) -> bool:
    """End an active tracking session."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        UPDATE tracking_sessions
        SET is_active = FALSE, end_time = CURRENT_TIMESTAMP
        WHERE session_token = ? AND is_active = TRUE
    ''', (session_token,))
    
    success = c.rowcount > 0
    conn.commit()
    conn.close()
    return success

def create_group(group_name: str, created_by: int) -> int:
    """Create a new location sharing group."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO groups (group_name, created_by)
        VALUES (?, ?)
    ''', (group_name, created_by))
    
    group_id = c.lastrowid
    conn.commit()
    conn.close()
    return group_id

def add_group_member(group_id: int, user_id: int, permissions: str = 'viewer') -> bool:
    """Add a user to a location sharing group."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO group_members (group_id, user_id, permissions)
            VALUES (?, ?, ?)
        ''', (group_id, user_id, permissions))
        
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    
    conn.close()
    return success

def get_group_members(group_id: int) -> List[Dict]:
    """Get all members of a location sharing group."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT u.id, u.username, gm.permissions, gm.joined_at
        FROM group_members gm
        JOIN users u ON gm.user_id = u.id
        WHERE gm.group_id = ?
    ''', (group_id,))
    
    results = c.fetchall()
    conn.close()
    
    return [
        {
            'id': user_id,
            'username': username,
            'permissions': permissions,
            'joined_at': joined_at
        }
        for user_id, username, permissions, joined_at in results
    ]

def save_game_score(user_id: int, score: int, rounds_completed: int) -> int:
    """Save a game session score."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO game_sessions (user_id, score, rounds_completed)
        VALUES (?, ?, ?)
    ''', (user_id, score, rounds_completed))
    
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_leaderboard(limit=10):
    try:
        import sqlite3
        import os
        
        # Create database directory if it doesn't exist
        db_dir = "data"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        conn = sqlite3.connect(f"{db_dir}/geoguesser.db")
        c = conn.cursor()
        
        # Create table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT DEFAULT 'Anonymous',
                score INTEGER,
                rounds INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Get leaderboard data
        c.execute('''
            SELECT username, score, rounds, timestamp 
            FROM leaderboard 
            ORDER BY score DESC 
            LIMIT ?
        ''', (limit,))
        
        results = c.fetchall()
        conn.close()
        
        return [
            {
                'username': row[0],
                'score': row[1],
                'rounds': row[2],
                'timestamp': row[3]
            }
            for row in results
        ]
        
    except Exception as e:
        print(f"Database error: {e}")
        return []  # Return empty list on error