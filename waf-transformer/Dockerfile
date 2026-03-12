FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY ingestion ./ingestion
COPY parsing ./parsing
COPY normalization ./normalization
COPY tokenization ./tokenization
COPY inference ./inference
COPY retraining ./retraining
COPY utils ./utils
COPY scripts ./scripts
COPY sample_data ./sample_data
COPY docs ./docs

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

