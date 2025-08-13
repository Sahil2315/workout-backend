from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    email: Optional[str]
    expYears: int
    expMonths: int
    level: str
    gender: str
    location: str
    weight: int
    height: int
    age: int
    specificAilment: str
    