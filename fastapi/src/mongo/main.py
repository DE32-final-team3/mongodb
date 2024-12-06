from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from src.mongo.crud import save_movie_to_db, fetch_movies_by_ids, fetch_all_movies
import logging

app = FastAPI()

# CORS 설정
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 기본 엔드포인트
@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API"}

# 영화 저장 엔드포인트
@app.post("/movies/save")
async def save_movie(movie: dict = Body(...)):
    try:
        result = await save_movie_to_db(movie)
        return result
    except Exception as e:
        logger.error(f"Error saving movie with ID {movie}: {e}")
        raise HTTPException(status_code=500, detail="Failed to save movie.")

# 영화 데이터 조회 엔드포인트
@app.get("/movies/all")
async def get_all_movies():
    try:
        movies = await fetch_all_movies()
        return {"movies": movies}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch movies.")

from fastapi import Query

# 영화 id 리스트 가져와 데이터 조회
@app.get("/movies/list")
async def get_movies_by_ids(movie_ids: list[int] = Query(...)):
    try:
        movies = await fetch_movies_by_ids(movie_ids)
        if not movies:
            return {"message": "No movies found for the provided IDs."}
        return {"movies": movies}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch movies.")

# @app.get("/movies/list")
# async def get_movies_by_ids(movie_ids: list[int] = Query(...)):
#     logging.info(f"Received request for movie IDs: {movie_ids}")
#     try:
#         movies = await fetch_movies_by_ids(movie_ids)
#         if not movies:
#             logging.warning(f"No movies found for provided IDs: {movie_ids}")
#             return {"message": "No movies found for the provided IDs."}
#         logging.info(f"Movies successfully fetched: {movies}")
#         return {"movies": movies}
#     except Exception as e:
#         logging.error(f"Exception in /movies/list: {e}")
#         raise


# 사용자 정의 예외 핸들러
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return {"detail": str(exc)}
