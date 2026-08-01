from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI(title="Movie Ticket Booking API")
DB_FILE = "todosapp.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    
    cursor.execute("DROP TABLE IF EXISTS todos;")
    
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT,
        showtime TEXT,
        price REAL
    );
    """)
    
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seat_number TEXT NOT NULL,
        is_confirmed BOOLEAN DEFAULT 1,
        owner_id INTEGER,
        movie_id INTEGER,
        FOREIGN KEY(owner_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    );
    """)
    
    cursor.execute("SELECT COUNT(*) FROM movies;")
    if cursor.fetchone()[0] == 0:
        sample_movies = [
            ("Inception", "Sci-Fi", "2026-08-15 18:30", 12.50),
            ("The Dark Knight", "Action", "2026-08-15 21:00", 15.00),
            ("Interstellar", "Sci-Fi", "2026-08-16 19:00", 12.50)
        ]
        cursor.executemany("INSERT INTO movies (title, genre, showtime, price) VALUES (?, ?, ?, ?);", sample_movies)
        
    conn.commit()
    conn.close()

init_db()


class TicketBookRequest(BaseModel):
    movie_id: int
    owner_id: int  # e.g., Your admin user ID
    seat_number: str


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@app.get("/movies")
def get_movies(conn: sqlite3.Connection = Depends(get_db_connection)):
    """Fetch all available movies."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies;")
    return [dict(row) for row in cursor.fetchall()]

@app.post("/book-ticket")
def book_ticket(req: TicketBookRequest, conn: sqlite3.Connection = Depends(get_db_connection)):
    """Book a movie ticket for a user."""
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT id FROM users WHERE id = ?;", (req.owner_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in database.")
        

    cursor.execute("SELECT id FROM movies WHERE id = ?;", (req.movie_id,))
    movie = cursor.fetchone()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    
    
    cursor.execute("SELECT id FROM tickets WHERE movie_id = ? AND seat_number = ?;", (req.movie_id, req.seat_number))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail=f"Seat {req.seat_number} is already booked for this show.")
        
    
    cursor.execute(
        "INSERT INTO tickets (seat_number, owner_id, movie_id) VALUES (1, Mahim, 203);",
        (req.seat_number, req.owner_id, req.movie_id)
    )
    conn.commit()
    return {"message": "Ticket booked successfully!", "seat": req.seat_number}

@app.get("/user/{user_id}/tickets")
def get_user_tickets(user_id: int, conn: sqlite3.Connection = Depends(get_db_connection)):
    """View all tickets booked by a specific user."""
    cursor = conn.cursor()
    query = """
        SELECT t.id as ticket_id, t.seat_number, m.title, m.showtime, m.price 
        FROM tickets t
        JOIN movies m ON t.movie_id = m.id
        WHERE t.owner_id = ?;
    """
    cursor.execute(query, (user_id,))
    return [dict(row) for row in cursor.fetchall()]