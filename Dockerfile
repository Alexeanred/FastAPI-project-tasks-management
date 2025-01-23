# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /fastapi-app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app/ ./app/

# Expose the app's port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
