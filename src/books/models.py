from sqlmodel import SQLModel, Field, Column
# This imports the PostgreSQL dialect from SQLAlchemy, which is used to define PostgreSQL-specific column types.
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
# This is used to generate a unique identifier for each book.
from uuid import UUID
import uuid
from typing import Optional

# You define models as Python classes that inherit from SQLModel.


class Book(SQLModel, table=True):
    # SQLModel is a base class for all SQLAlchemy models which is used to define the structure of the table in the database. The table=True argument indicates that this model should be treated as a database table.
    __tablename__ = "books"  # This is the name of the table in the database.
    uid: UUID = Field(  # Field lets u define the properties of the column in a more Pythonic way. It is used for simple columns (PK, FK, etc.). It is a shorthand for defining columns in SQLModel.
        sa_column=Column(  # sa_column lets you define exactly how the column should be created in the DB, using SQLAlchemy’s Column(). More explicit, used for complex columns (PK, UUID)
            # Tells the database what kind of value to store (column type).
            pg.UUID,
            nullable=False,
            primary_key=True,
            # Tells SQLAlchemy “if no value is provided for this field, generate one automatically.”
            default=uuid.uuid4
        )
    )
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    published_date: Optional[str]
    page_count: Optional[int]
    language: Optional[str]
    # Shorthand, works for simple columns (timestamp + default)
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):  # This method is used to define how the object should be represented as a string. It is useful for debugging and logging purposes.It is called when you print the object or when you use it in a string context.
        return f"<Book{self.title}>"

    # now we have created a database model for our book.
    # now we have to find a way to create this in our database. we can do that by using the init_db function in main.py using metadata of SQLModel.
