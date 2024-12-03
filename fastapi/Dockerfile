FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

EXPOSE 8000

CMD ["uvicorn", "src.mongo.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

