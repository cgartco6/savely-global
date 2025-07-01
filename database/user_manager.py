import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("database", "savely_global.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 email TEXT UNIQUE,
                 country TEXT,
                 signup_date DATE,
                 last_login DATE,
                 points INTEGER DEFAULT 0,
                 ad_views_today INTEGER DEFAULT 0,
                 is_premium INTEGER DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
                 id INTEGER PRIMARY KEY,
                 title TEXT,
                 description TEXT,
                 ingredients TEXT,
                 instructions TEXT,
                 nutrition TEXT,
                 country TEXT,
                 sa_flavor TEXT,
                 image_path TEXT,
                 video_path TEXT,
                 created_date DATE,
                 is_premium INTEGER DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS ad_views (
                 id INTEGER PRIMARY KEY,
                 user_id INTEGER,
                 brand TEXT,
                 cpm REAL,
                 view_date DATE)''')
    
    conn.commit()
    conn.close()

def save_recipes(recipes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().date()
    
    for recipe in recipes:
        c.execute('''INSERT INTO recipes 
                     (title, description, ingredients, instructions, nutrition, country, sa_flavor, 
                      image_path, video_path, created_date, is_premium)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (recipe['title'], 
                  recipe['description'],
                  json.dumps(recipe['ingredients']),
                  json.dumps(recipe['instructions']),
                  recipe.get('nutrition', ''),
                  recipe['country'],
                  recipe['sa_flavor'],
                  recipe.get('image_path', ''),
                  recipe.get('video_path', ''),
                  today,
                  0))  # Free by default
    
    conn.commit()
    conn.close()

def get_users_for_rewards():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE points > 0")
    users = c.fetchall()
    conn.close()
    return [user[0] for user in users]

def record_ad_view(user_id, brand, cpm):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().date()
    
    # Record ad view
    c.execute('''INSERT INTO ad_views (user_id, brand, cpm, view_date)
                 VALUES (?, ?, ?, ?)''', (user_id, brand, cpm, today))
    
    # Update user's daily ad count
    c.execute('''UPDATE users SET ad_views_today = ad_views_today + 1 
                 WHERE id = ?''', (user_id,))
    
    conn.commit()
    conn.close()

def reward_user_for_ad(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Add points
    c.execute('''UPDATE users SET points = points + 20 WHERE id = ?''', (user_id,))
    
    conn.commit()
    conn.close()
