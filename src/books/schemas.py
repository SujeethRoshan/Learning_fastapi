# This is better than keeping them in main.py, because now multiple parts of the app can reuse these schemas.
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class Book(BaseModel):
    uid: uuid.UUID
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    published_date: Optional[str]
    page_count: Optional[int]
    language: Optional[str]
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None


class BookUpdateModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    page_count: Optional[int]
    language: Optional[str]
