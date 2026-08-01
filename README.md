# 🎬 Movie Ticket FastAPI

A RESTful Movie Ticket Booking API built with **FastAPI**. This project allows users to browse movies, book tickets, manage reservations, and interact with a simple movie ticketing system.


## 🚀 Features

- 🎥 View all available movies
- 🔍 Search movies by title
- ➕ Add new movies
- ✏️ Update movie information
- ❌ Delete movies
- 🎫 Book movie tickets
- 📋 View booked tickets
- 🔄 Update ticket bookings
- 🗑️ Cancel booked tickets
- ⚡ FastAPI automatic interactive documentation
- 📦 Pydantic schema validation
- 🛡️ Request and response validation
- 📚 RESTful API architecture

---

## 📁 Project Structure

```
Movie-Ticket-FastApi/
│
├── app.py          # FastAPI application
├── main.py         # API routes
├── schema.py       # Pydantic schemas
├── Ticket.app      # Project configuration
└── README.md
```

---

## 🛠️ Technologies Used

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Movie-Ticket-FastApi.git
```

Move into the project folder

```bash
cd Movie-Ticket-FastApi
```

Install dependencies

```bash
pip install fastapi uvicorn
```

Run the server

```bash
uvicorn main:app --reload
```

---

## 🌐 API Documentation

After running the server:

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 📌 Example Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /movies | Get all movies |
| GET | /movies/{id} | Get movie by ID |
| POST | /movies | Add a new movie |
| PUT | /movies/{id} | Update movie |
| DELETE | /movies/{id} | Delete movie |
| POST | /tickets | Book a ticket |
| GET | /tickets | View booked tickets |
| DELETE | /tickets/{id} | Cancel booking |

---

## 📦 Example JSON

```json
{
    "movie_name": "Avengers: Endgame",
    "show_time": "7:30 PM",
    "seat_number": "A12",
    "price": 450
}
```

---

## 👨‍💻 Author

**Hredoy Hadi**

Computer Science & Engineering

---

## 📄 License

This project is developed for educational and learning purposes.
