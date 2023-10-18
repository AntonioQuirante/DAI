from django.db import models
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import os

class Product(BaseModel):
    _id: Optional[str]
    title: str
    price: float
    description: str
    category: str
    image: Optional[str] = None
    rating: Rating

class Rating(BaseModel):
    rate: float = Field(ge=0., lt=5.)
    count: int = Field(ge=1)

class Purchase(BaseModel):
    _id: Any
    user: EmailStr
    date: datetime
    products: list