FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

RUN pip install cachetools==4.2.4 requests==2.26.0

COPY ./app /app
