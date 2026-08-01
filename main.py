import sqlite3
from fastapi import FastAPI, HTTPException, status
from typing import Literal
from schemas import MovieCreate, MovieUpdate

app = FastAPI()
DATABASE = "movies.db"


def get_db_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
def startup():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            director TEXT NOT NULL,
            genre TEXT NOT NULL,
            duration INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()



@app.get("/movies/sort", status_code=status.HTTP_200_OK)
def sort_movies(
    sort_by: Literal["duration", "rating"] = "rating",
    order: Literal["asc", "desc"] = "desc"
):
    conn = get_db_conn()
    cursor = conn.cursor()
    

    query = f"SELECT * FROM movies ORDER BY {sort_by} {order.upper()}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


@app.get("/movies", status_code=status.HTTP_200_OK)
def get_movies():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]



@app.get("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def get_movie(movie_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE movie_id = ?", (movie_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Movie not found")
    return dict(row)


@app.post("/create_movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    conn = get_db_conn()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT 1 FROM movies WHERE movie_id = ?", (movie.movie_id,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")
    
    cursor.execute(
        "INSERT INTO movies (movie_id, title, director, genre, duration, rating) VALUES (?, ?, ?, ?, ?, ?)",
        (movie.movie_id, movie.title, movie.director, movie.genre, movie.duration, movie.rating)
    )
    conn.commit()
    conn.close()
    return movie



@app.put("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def update_movie(movie_id: int, movie: MovieUpdate):
    conn = get_db_conn()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT 1 FROM movies WHERE movie_id = ?", (movie_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Movie not found")
    
    cursor.execute(
        "UPDATE movies SET title = ?, director = ?, genre = ?, duration = ?, rating = ? WHERE movie_id = ?",
        (movie.title, movie.director, movie.genre, movie.duration, movie.rating, movie_id)
    )
    conn.commit()
    conn.close()
    
    return {"movie_id": movie_id, **movie.dict()}



@app.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def delete_movie(movie_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM movies WHERE movie_id = ?", (movie_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Movie not found")
    
    cursor.execute("DELETE FROM movies WHERE movie_id = ?", (movie_id,))
    conn.commit()
    conn.close()
    
    return {"message": f"Movie with ID {movie_id} has been deleted successfully."}