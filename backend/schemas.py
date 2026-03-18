from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_defined: bool = False

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    original_description: str
    amount: float
    date: datetime
    user_id: int
    category_id: Optional[int] = None
    categorized_by: Optional[str] = None
    raw_data_hash: str

class TransactionCreate(BaseModel):
    user_id: int
    original_description: str
    amount: float
    date: str # Use string for input, convert to datetime in main.py
    raw_data_hash: str

class Transaction(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
