FROM python:3.8

WORKDIR /app

COPY ./server/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./server /app

CMD ["uvicorn", "youtube_collector:app", "--host", "0.0.0.0", "--port", "8000"]