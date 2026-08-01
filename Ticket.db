from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hash_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    
    tickets = relationship("Tickets", back_populates="owner")


class Movies(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String)
    showtime = Column(String)  # e.g., "2026-08-15 18:30"
    price = Column(Float, default=10.0)

    tickets = relationship("Tickets", back_populates="movie")


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, nullable=False)
    is_confirmed = Column(Boolean, default=True)
    
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

    owner = relationship("Users", back_populates="tickets")
    movie = relationship("Movies", back_populates="tickets")


DROP TABLE IF EXISTS todos;

-- Create the new Movies catalog
CREATE TABLE movies (
    id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    genre VARCHAR,
    showtime VARCHAR,
    price REAL,
    PRIMARY KEY (id)
);

CREATE TABLE tickets (
    id INTEGER NOT NULL,
    seat_number VARCHAR NOT NULL,
    is_confirmed BOOLEAN DEFAULT 1,
    owner_id INTEGER,
    movie_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(owner_id) REFERENCES users (id),
    FOREIGN KEY(movie_id) REFERENCES movies (id)
);


