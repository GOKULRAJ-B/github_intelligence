FROM python:3.11-slim

WORKDIR /app

COPY consumers/pr_consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "consumers/pr_consumer/app.py"]