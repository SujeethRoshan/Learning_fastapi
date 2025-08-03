# creating __init__.py under src/ makes it a package.
from fastapi import FastAPI
# we need to  attach your book_router to your app.
from src.books.routes import book_router
# this is used to create an async context manager for the database session. which is responsible for mangaing the database connection and lifecycle.
from contextlib import asynccontextmanager
from src.db.main import init_db


# This decorator tells FastAPI to treat this function as a lifecycle handler.
@asynccontextmanager
# This function receives the FastAPI app instance when the app is created.
async def lifespan(app: FastAPI):
   # print(f"Starting up the application...") this is a example of a startup event. and this is how we can create database connection at start of our server.
    # Initialize the database connection. await here makes sure that the database is initialized before the application starts handling requests.
    await init_db()
    yield
    # print(f"Shutting down the application...")


version = "v1"
app = FastAPI(
    title="Bookly",
    description="A simple book management API",
    version=version,
    # This is a context manager that allows you to run code at the startup and shutdown of your FastAPI application.
    lifespan=lifespan
)
# the above code initializes a FastAPI application with a title, description, and version. we will see them in swagger UI.

# tags Used to group endpoints in Swagger docs under “books”

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
# above here, This is attaching your book_router to your app.
# Now lets start using a persistent database
# we are using postgresql as our database. in order to talk to the database we need to use an ORM (Object Relational Mapper) .
# ORM is translates between your python code and the database.
# SQLAlchemy is a popular ORM for Python.
# SQLModel is used becuase it is built on top of SQLAlchemy and Pydantic, which makes it easier to work with databases in FastAPI applications.
# async DBAPI is a standard interface for connecting to databases in Python. It is like a driver for the database.
# pip install asyncpg
# put ur environment variables in .env file then we need to access them in our code. There are many ways to access those env variable and to be specific with fastapi we can use pydantic settings.
# created config.py file to read the environment variables from the .env file.
# once that is done then we shall see how to connect to our database using our SQLModel. Lets install SQLModel.pip install sqlmodel.
# then after that create a db folder and it is a package as well.
