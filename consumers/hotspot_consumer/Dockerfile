FROM python:3.11-slim

WORKDIR /app

COPY consumers/hotspot_consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "consumers/hotspot_consumer/app.py"]