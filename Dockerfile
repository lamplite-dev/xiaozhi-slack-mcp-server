FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000 for the Bridge to talk to
EXPOSE 8000

# Start the SSE Server
CMD ["uvicorn", "main:mcp", "--host", "0.0.0.0", "--port", "8000"]
