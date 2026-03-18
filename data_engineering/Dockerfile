FROM python:3.9-slim-buster

WORKDIR /app/data_engineering

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "etl_pipeline.py"]
