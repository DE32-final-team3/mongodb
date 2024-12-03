import requests
from src.mongo.models import Movie
from src.mongo.database import engine

# 영화 저장 함수
async def save_movie_to_db(movie_id: int):
    # 기존 데이터 확인
    existing_movie = await engine.find_one(Movie, Movie.movie_id == movie_id)
    if existing_movie:
        return {"message": f"Movie '{existing_movie.title}' already exists in the database."}

    # DETAIL API 호출
    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ko-KR"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNmZlYzEwOGU3M2Y3YmVmNTkzYzM3N2RjMzdjYjcyZCIsIm5iZiI6MTczMjg2MjU3NC43Miwic3ViIjoiNjc0OTYyNmU0OTE5MDljMWI3OWRlY2VkIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.aumSeBsjfSdLck30QaMJjzeLi7ZZ4CMBOZS20p_AVdw"
    }
    detail_response = requests.get(detail_url, headers=headers)
    detail_data = detail_response.json()

    # CREDIT API 호출
    credit_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ko-KR"
    credit_response = requests.get(credit_url, headers=headers)
    credit_data = credit_response.json()

    # 데이터 정리
    genres = [genre["name"] for genre in detail_data.get("genres", [])]
    cast = sorted(
        [{"cast_id": c["cast_id"], "name": c["name"]} for c in credit_data.get("cast", [])],
        key=lambda x: x["cast_id"]
    )[:8]
    director = next(
        (
            {"id": crew["id"], "name": crew["name"]}
            for crew in credit_data.get("crew", [])
            if crew.get("job") == "Director"
        ),
        None
    )

    # MongoDB 저장
    movie = Movie(
        movie_id=detail_data["id"],
        title=detail_data.get("title"),
        original_title=detail_data.get("original_title"),
        overview=detail_data.get("overview"),
        poster_path=detail_data.get("poster_path"),
        original_country=detail_data.get("origin_country"),
        genres=genres,
        release_date=detail_data.get("release_date"),
        cast=cast,
        director=director,
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