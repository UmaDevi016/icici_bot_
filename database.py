import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class ConversationDB:
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                context_chunks TEXT
            )
        ''')
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    
    def create_session(self, session_id: str) -> bool:
        """Create a new conversation session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO sessions (session_id, created_at, last_activity)
                VALUES (?, ?, ?)
            ''', (session_id, datetime.now(), datetime.now()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating session: {e}")
            return False
    
    def add_conversation(self, session_id: str, user_message: str, 
                        bot_response: str, context_chunks: List[str] = None) -> bool:
        """Add a conversation to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert context chunks to JSON string
            context_json = json.dumps(context_chunks) if context_chunks else None
            
            cursor.execute('''
                INSERT INTO conversations (session_id, user_message, bot_response, context_chunks)
                VALUES (?, ?, ?, ?)
            ''', (session_id, user_message, bot_response, context_json))
            
            # Update session last activity
            cursor.execute('''
                UPDATE sessions SET last_activity = ? WHERE session_id = ?
            ''', (datetime.now(), session_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding conversation: {e}")
            return False
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_message, bot_response, timestamp, context_chunks
                FROM conversations
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            history = []
            for row in rows:
                context_chunks = json.loads(row[3]) if row[3] else []
                history.append({
                    'user_message': row[0],
                    'bot_response': row[1],
                    'timestamp': row[2],
                    'context_chunks': context_chunks
                })
            
            return list(reversed(history))  # Return in chronological order
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    def get_recent_context(self, session_id: str, limit: int = 5) -> str:
        """Get recent conversation context as a formatted string"""
        history = self.get_conversation_history(session_id, limit)
        
        context = ""
        for conv in history:
            context += f"User: {conv['user_message']}\n"
            context += f"Assistant: {conv['bot_response']}\n\n"
        
        return context.strip()
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a conversation session and all its messages"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
            cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """Clean up sessions older than specified days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete old conversations
            cursor.execute('''
                DELETE FROM conversations 
                WHERE session_id IN (
                    SELECT session_id FROM sessions 
                    WHERE last_activity < datetime('now', '-{} days')
                )
            '''.format(days))
            
            # Delete old sessions
            cursor.execute('''
                DELETE FROM sessions 
                WHERE last_activity < datetime('now', '-{} days')
            '''.format(days))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deleted_count
        except Exception as e:
            print(f"Error cleaning up old sessions: {e}")
            return 0

if __name__ == "__main__":
    # Test the database
    db = ConversationDB()
    
    # Test session creation
    session_id = "test_session_123"
    db.create_session(session_id)
    
    # Test adding conversation
    db.add_conversation(
        session_id, 
        "What is ICICI Insurance?", 
        "ICICI Insurance is a leading insurance company...",
        ["chunk1", "chunk2"]
    )
    
    # Test getting history
    history = db.get_conversation_history(session_id)
    print(f"History: {history}")
    
    print("Database test completed")
