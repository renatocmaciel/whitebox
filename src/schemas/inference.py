from datetime import datetime
from typing import Any, Dict, Union
from pydantic import BaseModel
from src.schemas.base import ItemBase


class InferenceBase(BaseModel):
    model_id: str
    timestamp: Union[str, datetime]
    features: Dict[str, Any]
    raw: Dict[str, Any]
    prediction: Dict[str, Any]
    actuals: Dict[str, Any]


class Inference(InferenceBase, ItemBase):
    pass


class InferenceCreate(InferenceBase):
    pass