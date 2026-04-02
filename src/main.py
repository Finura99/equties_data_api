from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from src.schemas import PriceResponse, TopMoverResponse
from src.services import validate_symbol, get_price_from_db, get_top_movers_from_db


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
    return df.to_dict(orient="records") #converts df to dict for fastapi to turn it into json format.

@app.get("/prices/{symbol}", response_model=PriceResponse) ##get all prices 
def get_price(symbol: str): ##uses database path

    symbol = validate_symbol(symbol) ##validate before hitting the business logic - db backed > using csv or cached data.

    result = get_price_from_db(symbol) #sends flow to the service where db and validation is involved, queries to see if symbol matches in sql.

    if result is None:
       raise HTTPException(status_code=404, detail="Symbol not found")
    
    return result
    
##fastapi will serialise the dict (result) and respond it back as a JSON array of object/s.


@app.get("/top-movers", response_model=list[TopMoverResponse])
def get_top_movers(limit: int = 5):

    ## cached in-memory data instead of repeatedly hitting the disk but below we use a sql backed flow.

    result = get_top_movers_from_db(limit) # endpoint relies on sql now rather than cached memory

    return result # fully db backed flow
