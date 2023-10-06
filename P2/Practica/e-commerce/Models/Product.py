from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from Models.Rating import Rating
import os

class Product(BaseModel):
    _id: Optional[str]
    title: str
    price: float
    description: str
    category: str
    image: Optional[str] = None
    rating: Rating