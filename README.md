
# ENDPOINTS
1. GET /prices -> uses cached csv bulk read
2. GET /prices/{symbol} -> SQL single-symbol lookup
3. GET /top-movers -> SQL analytics query
4. GET /stats 

Intentially using a transitional architecture to understand the different types of system thinking.

# Equities Data API

# What it does
A backend API built with FastAPI that provides stock price, top movers, and aggregated statistics using both CSV in-memory data cache and SQL flow using SQLite.

# Features
- Retrieves all prices (CSV cached and in-memory)
- Retrieves a single symbol (SQLite)
- Get top movers (SQL computation)
- Get aggregated statistics (SQL)

# Tech stack
- Python
- FastAPI
- SQLite
- Pandas
- Pytest

# Setup

'''bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Run API with 

'''uvicorn src.main:app --reload

Run Tests with 

'''python -m pytest -v

-------------------------------------


## Notes
- have been using request and cached data loaded once by the app in top mvoers and/bulk endpoints.
- single-symbol lookup uses SQLite.

-------------------------------------
# Architecture

- main.py handles routing and HTTP logic
- schema layer handles the response models
- service layer handles the db queries and business or validation logics.

