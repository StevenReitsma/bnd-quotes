from datetime import datetime
from pydantic import BaseModel


class Quote(BaseModel):
    Date: datetime
    Close: float
    Ask: float
    Bid: float
