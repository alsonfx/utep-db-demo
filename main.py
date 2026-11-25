from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import get_connection, init_db

# Establish our app as a fastapi app
app = FastAPI(title="UTEP CS 4342 Study Tracker")
init_db()

# Telling the project, where to save our HTML/ frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

# tells us the structure of database questions when adding
class QuestionCreate(BaseModel):
    topic_id: int
    prompt: str
    difficulty: str = "Medium"

# Update operation, allows to collect data to change existing items in db
class QuestionUpdate(BaseModel):
    topic_id: int
    prompt: str
    difficulty: str

# tells the app where we are going to display our information
# in other words, where the frontend is located
@app.get("/") # homepage
def serve_frontend():
    return FileResponse("static/index.html")


# display the topics of our application
@app.get("/topics") # homepage/topics
def list_topics():
    conn = get_connection()
    rows = conn.execute("SELECT topic_id, name FROM topics ORDER BY topic_id;").fetchall()
    conn.close()
    return [dict(row) for row in rows]

# do the same for questions
@app.get("/questions")
def list_questions():
    conn = get_connection()
    rows = conn.execute("""
        SELECT q.question_id, q.topic_id, t.name AS topic_name, q.prompt, q.difficulty
        FROM questions q
        JOIN topics t ON q.topic_id = t.topic_id
        ORDER BY q.question_id DESC;
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# This is the app wrapper for adding new questions
@app.post("/questions", status_code=201)
def create_question(q: QuestionCreate):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO questions (topic_id, prompt, difficulty) VALUES (?, ?, ?);",
            (q.topic_id, q.prompt, q.difficulty),
        )
        conn.commit()
        return {"question_id": cursor.lastrowid, "message": "Question created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# wrapper for updating questions in our database
@app.put("/questions/{question_id}")
def update_question(question_id: int, q: QuestionUpdate):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "UPDATE questions SET topic_id = ?, prompt = ?, difficulty = ? WHERE question_id = ?;",
            (q.topic_id, q.prompt, q.difficulty, question_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Question not found")
        return {"message": "Question updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


# app wrapper for deleting items
@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM questions WHERE question_id = ?;", (question_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted"}