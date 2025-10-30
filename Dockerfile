FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y bash netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x backend/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./backend/entrypoint.sh"]