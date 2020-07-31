FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

RUN pip install cachetools==4.1.1 requests==2.24.0

COPY ./app /app
