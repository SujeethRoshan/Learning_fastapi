# This is where your actual endpoints now live. Instead of defining everything in main.py, they’re grouped in a router:
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import Optional  # Import Optional for optional query parameters
# Import BaseModel for data validation and serialization.
from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from typing import List
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from uuid import UUID

book_router = APIRouter()
# So instead of @app.get(...), you now use @book_router.get(...).
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books
# So here if say just Book in the response model it will give u internal error saying that pydatic is expecting it to be a dictionary and not a list. since our books is a list of dictionaries. we need to specify that the response model is a list of Book instances.


# FastAPI returns 201 Created only if the route finishes without errors.
@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    # new_book = book_data.model_dump()  # Convert Pydantic model to plain dictionary
    # books.append(new_book)  # Add the new book to the list books.
    new_book = await book_service.create_book(book_data, session)
    return new_book  # Return the newly created book in the HTTP response.
# curl -X POST http://127.0.0.1:8000/api/v1/books/ \
#   -H "Content-Type: application/json" \
#   -d '{
#     "title": "Head First HTML5 Programming",
#     "author": "Eric T Freeman",
#     "publisher": "O'\''Reilly Media",
#     "published_date": "2011-01-21",
#     "page_count": 3006,
#     "language": "English"
#   }'

# lets try get single book by id.


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(book_uid: UUID, session: AsyncSession = Depends(get_session)) -> dict:
    # for book in books:
    #     if book["id"] == book_id:
    #         return book
    book = await book_service.get_book(book_uid, session)
    if book:
        return book.dict()  # Convert SQLModel instance to dictionary
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(book_uid: UUID, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
    # for book in books:
    #     if book['id'] == book_id:
    #         book['title'] = book_update_data.title
    #         book['publisher'] = book_update_data.publisher
    #         book['page_count'] = book_update_data.page_count
    #         book['language'] = book_update_data.language

    #         return book
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book.dict()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")

# curl -X PATCH "http://localhost:8000/books/1" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "title": "Updated Title",
#     "author": "New Author",
#     "publisher": "New Publisher",
#     "page_count": 456,
#     "language": "French"
# }'


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: UUID, session: AsyncSession = Depends(get_session)) -> None:
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete:
        # Don't return anything for 204 response
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

# curl -X DELETE "http://localhost:8000/books/1"
