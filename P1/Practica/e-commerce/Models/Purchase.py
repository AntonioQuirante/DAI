from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import os

class Purchase(BaseModel):
	_id: Any
	user: EmailStr
	date: datetime
	products: list