FROM python:3.11-slim

WORKDIR /app

# System
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python", "init.py"]
CMD ["python", "main.py"]
