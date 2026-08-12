from src.pyugioh.models.base_card import BaseCard
from src.pyugioh.pygo_core import constants
from pydantic import field_validator,ValidationError

class MonsterCard(BaseCard):
    type: str
    level: int
    attack: int
    defense: int

    def __init__(self, **data):
        data['attack'] = data.pop("atk",0)
        data['defense'] = data.pop("def",0)
        super().__init__(**data)

    @field_validator("type")
    @classmethod
    def validate_type(cls,v: str) -> str:
        if v not in constants.PYUGIOH_TYPE_VALUES_MONSTER:
            raise ValidationError(f"type must be one of the following: {constants.PYUGIOH_TYPE_VALUES_MONSTER}")
        return v