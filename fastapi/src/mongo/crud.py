import requests
from src.mongo.models import Movie
from src.mongo.database import engine
from typing import Dict, List

# 영화 저장 함수
async def save_movie_to_db(movie_data: Dict):
    # 기존 데이터 확인
    existing_movie = await engine.find_one(Movie, Movie.movie_id == movie_id)
    if existing_movie:
        return {"message": f"Movie '{existing_movie.title}' already exists in the database."}

    #필요항목 확인단계
    required_fields = ["movie_id", "title", "original_title", "overview", "poster_path", "original_country", "genres", "release_date", "cast", "director"]
    missing_fields = [field for field in required_fields if field not in movie_data]
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )

    # MongoDB 저장
    movie = Movie(
        movie_id=movie_data["id"],
        title=movie_data["title"],
        original_title=movie_data["original_title"],
        overview=movie_data["overview"],
        poster_path=movie_data["poster_path"],
        original_country=movie_data["origin_country"],
        genres=movie_data['genres'],
        release_date=movie_data["release_date"],
        cast=movie_data["cast"],
        director=movie_data["director"],
    )
    await engine.save(movie)
    return {"message": f"Movie '{movie.title}' has been saved to the database."}



# 모든 영화 데이터를 JSON으로 반환하는 함수
async def fetch_all_movies():
    # 모든 영화 데이터를 조회
    movies = await engine.find(Movie)

    # 영화 데이터를 리스트로 변환
    movie_data = []
    for movie in movies:
        # cast에서 name만 필터링
        filtered_cast_names = [c["name"] for c in movie.cast] if movie.cast else None
        
        # director에서 name만 필터링
        director_name = movie.director["name"] if movie.director else None

        # 영화 정보를 딕셔너리로 저장
        movie_data.append({
            "movie_id": movie.movie_id,
            "title": movie.title,
            "original_title": movie.original_title,
            # "overview": movie.overview,
            "poster_path": movie.poster_path,
            "genres": movie.genres,
            "cast": filtered_cast_names,
            "director": director_name,
            "original_country": movie.original_country,
            # "release_date": movie.release_date,
        })

    return movie_data


# 특정 movie_id 리스트에 해당하는 영화 데이터 가져오기
async def fetch_movies_by_ids(movie_ids: list[int]):
    movies = await engine.find(Movie, Movie.movie_id.in_(movie_ids))
    return [
        {
            "movie_id": movie.movie_id,
            "title": movie.title,
            "genres": movie.genres,
            # "director": movie.director,
            "director": movie.director.get("name") if movie.director else None,
            "poster_path": movie.poster_path,
            # "release_date": movie.release_date,
            # "cast": movie.cast,
            "cast": [member.get("name") for member in movie.cast] if movie.cast else [],
            "original_country": movie.original_country,
        }
        for movie in movies
    ]
