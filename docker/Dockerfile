# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2 (Postgres connector)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ /app/backend
COPY db/ /app/db

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit (or Flask later)
CMD ["streamlit", "run", "backend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
