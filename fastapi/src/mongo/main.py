from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from src.mongo.crud import save_movie_to_db
import logging

app = FastAPI() 

origins = ["*"]

app.add_middleware(
    CORSMiddleware,  
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API"}

@app.post("/movies/{movie_id}")
async def save_movie(movie_id: int):
    try:
        result = await save_movie_to_db(movie_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return {"detail": str(exc)}

