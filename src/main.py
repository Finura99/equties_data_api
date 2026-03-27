from pathlib import Path
import pandas as pd
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.schemas import PriceResponse, TopMoverResponse


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

@app.get("/prices/{symbol}", response_model=PriceResponse) ##get all prices
def get_price(symbol: str, request: Request):

    symbol = symbol.upper() #converts it to uppercase

    ##df = pd.read_csv(PRICES_PATH) ## loads csv and converts to a dataframe-- UPDATE: SLOWER THAN CACHE
    df = request.app.state.prices_df ## uses in memory data rather than exhaust disk i/o operations.

    filtered = df[df["symbol"] == symbol] #boolean check to see if it matches with our variable above

    if filtered.empty:
       return {
           "symbol" : symbol,
           "error" : "symbol not found"
       }
    
    row = filtered.iloc[0] #returns first series (one row)
    return row.to_dict() #API ready object
    
##fastapi will serialise the dict and respond it back as an array of JSON object/s.


## create an endpoint for top movers
@app.get("/top-movers", response_model=list[TopMoverResponse])
def get_top_movers(request: Request, limit: int = 5):

##load csv in df
    ##df = pd.read_csv(PRICES_PATH) #the api reads from the disk repeatedly in traffic ,not efficient.
    df = request.app.state.prices_df.copy() #avoids mutation, gives us local working df


    ## better approach is to load the data once at startup and then keep it in memory, so the request works on 
    ## cached data instead of repeatedly hitting the disk.

#avoids division by 0/ bad prev price
    df = df[df["prev_price"] > 0]

#calculate change_pct
    df["change_pct"] = (df["price"] - df["prev_price"]) / (df["prev_price"] * 100)

#sort descending
    top = df.sort_values("change_pct", ascending=False).head(limit) #take top n-> .head
#return list with dicts
    return top.to_dict(orient = "records")