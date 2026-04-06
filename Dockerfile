# base python environmment
FROM python:3.12-slim 

# where app lives inside the container
WORKDIR /app

# copy dependency file first
COPY requirements.txt .

# install packages
RUN pip install --no-cache-dir -r requirements.txt

# copy code
COPY . .

# app uses port 8000
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]



