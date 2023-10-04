from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import os

class Rating(BaseModel):
    rate: float = Field(ge=0., lt=5.)
    count: int = Field(ge=1)
