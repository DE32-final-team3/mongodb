# MongoDB 설계하는 방법

### 파일트리 설명
```python
├── README.md
├── fastapi
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── src
│   │   └── final_backend
│   │       ├── crud.py			# 데이터 베이스를 업데이트하는 CRUD
│   │       ├── database.py 		# MongoDB 엔진과의 연결
│   │       ├── main.py
│   │       ├── models.py 		# Movie class 정의 
│   │       └── router
│   │           ├── __init__.py
│   │           └── movie_router.py	#FastAPI 엔드포인트로 연결
│   └── tests # 비어있는 테스트 파일
│       └── __init__.py
└── mongodb
    └── docker-compose.yml
```
### MongoDB docker container 실행
```python
cd mongodb

docker compose up
```

### FastAPI docker container 실행
```python
cd fastapi

docker compose up
```
