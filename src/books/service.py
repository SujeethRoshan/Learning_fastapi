# Service class is going to have all our CRUD has all the logic related to CRUD with the database.
# AsyncSession is used to create a session for interacting with the database asynchronously.
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book


class BookService:
    # session is a medium provided by sqlmodel to interact with the database.It represents an asynchronous database session—a “conversation” with your database, where you can query, insert, update, or delete data using async/await syntax.It is not a connection to your database by itself.
    async def get_all_books(self, session: AsyncSession):
        # give selct() and then the model you want to select from. order_by(desc(Book.created_at)): This sorts the results by the created_at column in descending order.
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        # This returns the first book that matches the uid.
        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        # Book is your SQLModel/ORM model for the books table.**book_data_dict unpacks the dictionary, so it’s like calling:Book(title="Python 101", author="John")
        new_book = Book(**book_data_dict)
        # This doesn’t write to the database yet, it just prepares it. It just adds the new book to the session.
        session.add(new_book)
        await session.commit()  # This saves the new book to the database.
        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.one_or_none()
        if not book:
            return None  # or raise HTTPException(404, ...)
        # converts the Pydantic model into a Python dictionary, but only includes the fields that were actually sent by the user (i.e., fields that are not "unset").
        update_fields = update_data.model_dump(exclude_unset=True)
        for key, value in update_fields.items():
            setattr(book, key, value)
        # book = result.one_or_none() gets a book record from the database (or None if not found).The next lines like setattr(book, key, value) use this same book object to update its fields.setattr(book, "title", "New Title") is the same as writing book.title = "New Title"
        session.add(book)  # not strictly necessary, but safe
        await session.commit()
        await session.refresh(book)  # refresh to get updated data from DB
        return book

    async def delete_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.one_or_none()
        if not book:
            return False  # or raise HTTPException(404, ...)

        await session.delete(book)
        await session.commit()
        return True
