from django.db import models
from pydantic import BaseModel, EmailStr, Field, BaseConfig
from typing import Optional, Any
import datetime

import os

class CustomBaseConfig(BaseConfig):
    arbitrary_types_allowed = True

class Rating(BaseModel):
    rate: float = Field(ge=0., lt=5.)
    count: int = Field(ge=1)


class Product(BaseModel):
    _id: Optional[str]
    title: str
    price: float
    description: str
    category: str
    image: Optional[str] = None
    rating: Rating


class Purchase(BaseModel):
    _id: Any
    user: EmailStr
    date: datetime
    products: list

    class Config(CustomBaseConfig):
        arbitrary_types_allowed = True
