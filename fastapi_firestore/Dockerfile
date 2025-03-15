# Python version
FROM python:3.11-slim

# Working Directory
WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Main.py code
COPY . .
EXPOSE 8080

ENV PORT=8080

#Run the app
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT


