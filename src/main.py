from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager

from src.schemas import PriceResponse, TopMoverResponse, PriceCreate
from src.services import (
    validate_symbol,
    get_price_from_db,
    get_top_movers_from_db,
    get_price_stats_from_db, 
    get_price_with_company_from_db,
    get_price_from_postgres,
    create_price_in_postgres
    )


BASE_DIR = Path(__file__).resolve().parent.parent ##root directory
PRICES_PATH = BASE_DIR / "data" / "prices.csv"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading data at startup...") # before server starts

    app.state.prices_df = pd.read_csv(PRICES_PATH) #load the data in memory once

    yield

    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/health") #proves app is alive
def health():
    return {"status": "ok"}
    
@app.get("/prices")
def get_prices(request: Request):
    df = request.app.state.prices_df
    return df.to_dict(orient="records") #converts df to list of dicts for fastapi to turn it into json format.

@app.get("/prices/{symbol}", response_model=PriceResponse) ##get all prices 
def get_price(symbol: str): ##uses database path

    symbol = validate_symbol(symbol) ##validate before hitting the business logic - db backed > using csv or cached data.

    result = get_price_from_db(symbol) #sends flow to the service where db and validation is involved, queries to see if symbol matches in sql.

    if result is None:
       raise HTTPException(status_code=404, detail="Symbol not found")
    
    return result
    
##fastapi will serialise the dict (result) and respond it back as a JSON array of object/s.


@app.get("/top-movers", response_model=list[TopMoverResponse])
def get_top_movers(limit: int = 5) -> list:

    ## cached in-memory data instead of repeatedly hitting the disk but below we use a sql backed flow.

    result = get_top_movers_from_db(limit) # endpoint relies on sql now rather than cached memory

    return result # fully db backed flow

@app.get("/stats")
def get_stats():
    return get_price_stats_from_db()

@app.get("/prices/{symbol}/details")
def get_price_with_company(symbol: str):
    return get_price_with_company_from_db(symbol)

@app.get("/postgres/prices/{symbol}")
def get_prices_postgres(symbol:str):
    symbol = validate_symbol(symbol)

    result = get_price_from_postgres(symbol)

    if result is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    
    return result

@app.post("/postgres/prices", response_model=PriceCreate) # routing
def create_price(payload: PriceCreate):
    symbol = validate_symbol(payload.symbol) # validation

    result = create_price_in_postgres(
        symbol=symbol,
        price=payload.price,
        prev_price=payload.prev_price,
    ) # service layer

    if result.exists():
        raise HTTPException(status_code=409, detail=f"Symbol '{payload.symbol}' already exists")

    return result #dict response