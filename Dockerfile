# base python environmment
FROM python:3.12-slim 

# Update packages to fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# where app lives inside the container
WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# copy dependency file first
COPY requirements.txt .

# install packages
RUN pip install --no-cache-dir -r requirements.txt

# copy code
COPY . .

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# app uses port 8000
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]



