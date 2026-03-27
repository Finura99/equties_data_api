from pydantic import BaseModel

class PriceResponse(BaseModel):
    symbol: str
    price: float
    prev_price: str

class TopMoverResponse(BaseModel):
    symbol: str
    price: float
    prev_price: float
    change_pct: float