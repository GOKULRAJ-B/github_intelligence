FROM python:3.11-slim

WORKDIR /app

COPY consumers/churn_consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "consumers/churn_consumer/app.py"]