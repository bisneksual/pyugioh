from pydantic import BaseModel
from typing import Optional
from src.pyugioh.pygo_core import utils

class BaseCard(BaseModel):
    id: int
    name: str
    frame: str
    desc: str
    race: str
    set_code: Optional[str] = "N/A"

    def __init__(self,**data):
        data['frame'] = data.pop("frameType","N/A")
        data['desc'] = utils.sanitize_desc(data.get("desc","N/A"))
        super().__init__(**data)