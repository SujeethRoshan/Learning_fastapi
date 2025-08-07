# here we will create engine of sqlmodel to talk to our database. The engine is the component that manages the actual connection between your application and the database. You typically create the connection by using the create_engine function from SQLModel.
# since we are using asyncpg as our database driver, we need to use AsyncEngine.
# It creates a synchronous SQLAlchemy engine under the hood.
# text is used to execute raw SQL statements.
# sqlmodel.create_engine() by itself only creates a synchronous engine, not an async one.
from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
# Importing the Book model to create tables in the database.
from src.books.models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


engine = AsyncEngine(create_engine(url=Config.DATABASE_URL,
                                   # this line executed when module is imported.
                                   echo=True))


async def init_db():  # This defines an asynchronous function to initialize the database.
    # This function is used to initialize the database connection until the application is shut down.
    async with engine.begin() as conn:  # Opens an asynchronous connection to the database, engine.begin() creates a transaction block, meaning if any operations inside this block fail, they will be rolled back automatically. "con" is the connection object we will use to execute SQL commands. "with" keyword ensures that the connection is properly closed after the block is executed.
        # The query you saw is just a "ping" to the database.
        # statement = text("SELECT 'hello';") # This is a raw SQL statement that selects a string 'hello' from the database. It is used to test the connection to the database.
        # await is used to wait for the result of the asynchronous operation. await makes it non-blocking.
        # result = await conn.execute(statement)
        # .all() returns all rows fetched from the database.
        # print(result.all())

        # Now lets create a database model.
        # A database model is a class that represents a table in the database. It is used to define the structure of the table and the data types of its columns.
        # under books created a file called models.py
        # now let's create database tables in our database rather than just pinging it.
        await conn.run_sync(SQLModel.metadata.create_all)
        # metadata - This is a special object that keeps track of all your models (tables) that have been defined with SQLModel + table=True and imported somewhere in your project. and create_all - This method creates all tables in the database that are defined in the metadata. It will create the tables if they do not exist, and it will not modify existing tables. create_all is a synchronous method, so we use run_sync to run it in an asynchronous context.


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        # This specifies that the session will be an instance of AsyncSession, which is used for asynchronous operations.
        class_=AsyncSession,
        # This means that after committing a transaction, the session will not expire the objects, allowing you to access them without reloading from the database.
        expire_on_commit=False
    )

    # This creates an asynchronous context manager for the session. It ensures that the session is properly closed after use.
    async with Session() as session:
        # This yields the session object, allowing you to use it in your application code. The session will be automatically closed when the context manager exits.
        yield session
