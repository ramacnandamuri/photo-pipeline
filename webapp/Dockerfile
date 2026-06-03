FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime

COPY app.py .
COPY templates/ templates/

EXPOSE 5000

CMD ["python", "app.py"]