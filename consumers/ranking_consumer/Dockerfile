FROM python:3.11-slim

WORKDIR /app

COPY consumers/ranking_consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "consumers/ranking_consumer/app.py"]