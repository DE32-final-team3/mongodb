from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.final_backend.router.movie_router import movie_router
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

# movie_router 등록
app.include_router(movie_router)

# 사용자 정의 예외 핸들러
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return {"detail": str(exc)}