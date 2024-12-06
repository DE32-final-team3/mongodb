import requests
from fastapi import HTTPException
from src.mongo.models import Movie
from src.mongo.database import engine
from typing import Dict, List

# 영화 저장 함수
async def save_movie_to_db(movie_data: Dict):
    # 기존 데이터 확인
    existing_movie = await engine.find_one(Movie, Movie.movie_id == movie_data['movie_id'])
    if existing_movie:
        return {"message": f"Movie '{existing_movie.title}' already exists in the database."}

    #필요항목 확인단계
    required_fields = ["movie_id", "title", "original_title", "overview", "poster_path", "original_language", "genres", "release_date", "cast", "director"]
    missing_fields = [field for field in required_fields if field not in movie_data]
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    # MongoDB 저장
    movie = Movie(
        movie_id=movie_data["movie_id"],
        title=movie_data["title"],
        original_title=movie_data["original_title"],
        overview=movie_data["overview"],
        poster_path=movie_data["poster_path"],
        original_language=movie_data["original_language"],
        genres=movie_data['genres'],
        release_date=movie_data["release_date"],
        cast=movie_data["cast"],
        director=movie_data["director"],
    )
    await engine.save(movie)
    return {"message": f"Movie '{movie.title}' has been saved to the database."}
