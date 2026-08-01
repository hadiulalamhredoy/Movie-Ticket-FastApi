from pydantic import BaseModel, Field, PositiveInt
from typing import Literal

class MovieCreate(BaseModel):
    movie_id: int
    title: str
    director: str
    genre: Literal["action", "comedy", "drama", "thriller"]
    duration: PositiveInt  
    rating: float = Field(..., ge=0.0, le=5.0) 


class MovieUpdate(BaseModel):
    title: str
    director: str
    genre: Literal["action", "comedy", "drama", "thriller"]
    duration: PositiveInt
    rating: float = Field(..., ge=0.0, le=5.0)



    