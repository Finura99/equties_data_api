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

    app.state.prices_df = pd.read_csv(PRICES_PATH) #load the data in memory
    #app.state.trades_df = pd.read_csv(TRADES_PATH) #store it in app.state

    yield

    print("Shutting down...")

app = FastAPI(lifespan=lifespan)




@app.get("/health") #proves app is alive
def health():
    return {"status": "ok"}
    

@app.get("/prices")
def get_prices(request: Request):
    df = request.app.state.prices_df
    return df.to_dict(orient="records")


def get_price_from_df(df, symbol):

    result = df[df["symbol"] == symbol]

    if result.empty:
        return None
    row = result.iloc[0]

    return {
        "symbol": row["symbol"],
        "price": row["price"],
        "prev_price": row["prev_price"]
    }

@app.get("/prices/{symbol}", response_model=PriceResponse) ##get all prices 
def get_price(symbol: str): ##uses database path


    ##df = pd.read_csv(PRICES_PATH) ## loads csv and converts to a dataframe-- UPDATE: SLOWER THAN CACHE (line below)
    ##df = request.app.state.prices_df ## uses in memory data rather than exhaust disk i/o operations.
    symbol = validate_symbol(symbol) ##validate before hitting the business logic - db backed > using csv or cached data.

    result = get_price_from_db(symbol) #sends flow to the service where db and validation is involved, queries to see if symbol matches in sql.

    if result is None:
       raise HTTPException(status_code=404, detail="Symbol not found")
    
    return result
    
##fastapi will serialise the dict (result) and respond it back as a JSON array of object/s.


## create an endpoint for top movers
@app.get("/top-movers", response_model=list[TopMoverResponse])
def get_top_movers(request: Request, limit: int = 5):

##load csv in df
    ##df = pd.read_csv(PRICES_PATH) #the api reads from the disk repeatedly in traffic ,not efficient.
    ##df = request.app.state.prices_df.copy() #avoids mutation, gives us local working df
    ## better approach is to load the data once at startup and then keep it in memory, so the request works on 
    ## cached data instead of repeatedly hitting the disk.


    result = get_top_movers_from_db(limit) # endpoint relies on sql now rather than cached memory


#avoids division by 0/ bad prev price
    df = df[df["prev_price"] > 0]

#calculate change_pct and create new column 
    df["change_pct"] = ((df["price"] - df["prev_price"]) / df["prev_price"] * 100)

#sort descending
    top = df.sort_values("change_pct", ascending=False).head(limit) #take top n-> .head
#return list with dicts
    return result