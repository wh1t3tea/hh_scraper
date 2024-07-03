from pydantic import BaseModel
from typing import List, Dict

class DataModel(BaseModel):
    data: List[Dict]