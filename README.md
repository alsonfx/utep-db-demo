# UTEP CS 4342 — Study Question Bank

A full-stack CRUD demo application built with **Python**, **FastAPI**, **SQLite**, and vanilla **HTML/CSS/JS**. 

This project serves as an end-to-end reference architecture illustrating how modern web APIs interface with a relational database, enforce schema constraints, protect against SQL injection, and serve dynamic data to a frontend.

---

## Key Database Concepts Demonstrated

- **Foreign Key Enforcement**: SQLite requires `PRAGMA foreign_keys = ON;` per connection to enforce referential integrity.
- **Cascading Deletes**: `FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE`.
- **Domain Constraints**: `CHECK (difficulty IN ('Easy', 'Medium', 'Hard'))` to validate values at the database level.
- **Uniqueness Constraints**: `UNIQUE` constraint on topic names to prevent duplicate categories.
- **SQL Injection Prevention**: Parameterized queries using `?` placeholders for all dynamic inputs (`INSERT`, `UPDATE`, `DELETE`).
- **Relational Queries (JOINs)**: Uses an `INNER JOIN` across `questions` and `topics` to resolve topic IDs into human-readable labels.

---

## Project Structure

```text
utep-db-demo/
├── database.py         # Schema creation, DB connection helper, and seed data
├── main.py             # FastAPI backend with Pydantic models & CRUD endpoints
├── pyproject.toml      # Project metadata and dependencies (FastAPI, Uvicorn)
├── static/
│   └── index.html      # Responsive SPA frontend styled with UTEP palette
├── study_tracker.db    # SQLite database file (created automatically on startup)
└── uv.lock             # Deterministic dependency lockfile
```

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS topics (
    topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    prompt TEXT NOT NULL,
    difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')) DEFAULT 'Medium',
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);
```

### Default Seed Topics
1. ER Modeling
2. Normalization
3. SQL & Joins
4. DB Security

---

## Getting Started

### Prerequisites
- Python 3.14+ (or compatible 3.10+)
- [uv](https://docs.astral.sh/uv/) (recommended) or standard `pip`

### Option 1: Using `uv` (Recommended)

1. **Install dependencies and sync virtual environment:**
   ```bash
   uv sync
   ```

2. **Run the development server:**
   ```bash
   uv run uvicorn main:app --reload
   ```

### Option 2: Using standard Python `venv`

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

---

## Using the Application

- **Web UI**: Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
- **Interactive API Docs (Swagger UI)**: Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test endpoints interactively.
- **Alternative Docs (ReDoc)**: Open [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

---

## API Endpoints

| Method | Endpoint | Description | SQL Operation |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Serves the single-page frontend | N/A |
| `GET` | `/topics` | Returns all available study topics | `SELECT topic_id, name FROM topics` |
| `GET` | `/questions` | Returns all questions with topic names | `SELECT ... FROM questions JOIN topics` |
| `POST` | `/questions` | Inserts a new study question | `INSERT INTO questions ... VALUES (?, ?, ?)` |
| `PUT` | `/questions/{id}` | Updates an existing question | `UPDATE questions SET ... WHERE question_id = ?` |
| `DELETE` | `/questions/{id}` | Deletes a question by ID | `DELETE FROM questions WHERE question_id = ?` |

---

## Resetting the Database

To reset the database back to its fresh state with default topics:
1. Stop the running server (`Ctrl + C`).
2. Delete the `study_tracker.db` file.
3. Restart the server or run `python database.py` directly to re-initialize tables and seed data.
