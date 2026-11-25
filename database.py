import sqlite3 # <- importing sqlite, which allows to create a local database file

DB_NAME = "study_tracker.db" # naming our database

# used to connect to the database
def get_connection():
  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = sqlite3.Row
  conn.execute("PRAGMA foreign_keys = ON;")
  return conn

# used to create our database
def init_db():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS topics (
  topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
  );
  """)
  
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS questions (
  question_id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_id INTEGER NOT NULL,
  prompt TEXT NOT NULL,
  difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard'))
  DEFAULT 'Medium',
  FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
  );
  """)
  
  cursor.execute("""
  INSERT OR IGNORE INTO topics (topic_id, name)
  VALUES (1, 'ER Modeling'), (2, 'Normalization'), (3, 'SQL & Joins'), (4,
  'DB Security');
  """)

  conn.commit()
  conn.close()

  
if __name__ == "__main__":
  init_db()
  print("Database and tables initialized!")