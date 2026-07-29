FROM python:3.11-slim

WORKDIR /app

COPY consumers/commit_consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "consumers/commit_consumer/app.py"]