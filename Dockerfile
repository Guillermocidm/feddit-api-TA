FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ ./src/

ENV PORT=5000

EXPOSE ${PORT}

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]