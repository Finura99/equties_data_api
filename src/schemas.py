from pydantic import BaseModel

class PriceResponse(BaseModel):
    symbol: str
    price: float
    prev_price: float

class TopMoverResponse(BaseModel):
    symbol: str
    price: float
    prev_price: float
    change_pct: float


class PriceCreate(BaseModel):
    symbol: str
    price: float
    prev_price: float

## the last one is our input contract for post endpoint.