from pydantic import BaseModel
from typing import List, Dict

class StockBase(BaseModel):
    status: str
    purchased_amount: int
    purchased_status: str
    request_data: str
    company_code: str
    company_name: str
    open: float
    high: float
    low: float
    close: float
    performance_data: Dict[str, float]
    competitors: List[Dict[str, str]]

class StockUpdate(BaseModel):
    amount: int
