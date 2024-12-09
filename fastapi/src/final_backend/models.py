from odmantic import Model
from typing import List, Optional

class Movie(Model):
    movie_id: int
    title: str
    original_title: Optional[str] = None
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    original_language: Optional[str] = None 
    genres: List[int] = []
    release_date: Optional[str] = None
    cast: Optional[List[dict]] = None
    director: Optional[dict] = None
