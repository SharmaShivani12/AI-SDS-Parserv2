from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class SDSExtracted(BaseModel):
    product_name: Optional[str] = None
    supplier: Optional[str] = None
    cas_numbers: List[str] = []
    hazard_statements: List[str] = []
    precautionary_statements: List[str] = []
    signal_word: Optional[str] = None
    pictograms: List[str] = []

class SDSBase(BaseModel):
    id: int
    filename: str
    created_at: datetime
    supplier: Optional[str]
    extracted: SDSExtracted

    class Config:
        orm_mode = True

class SDSListItem(BaseModel):
    id: int
    filename: str
    created_at: datetime
    supplier: Optional[str]

    class Config:
        orm_mode = True

class SDSDetail(SDSBase):
    raw_text: str
