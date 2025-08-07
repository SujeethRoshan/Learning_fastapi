# Learning_fastapi
I am learning fastapi with real world concepts so adding the codes for my reference

first when application starts __init__.py file is executed and router is attached.
It loads routers (book_router), sets up the database connection (via init_db()), and runs any startup events.
Since, we are suing async context manager decorator above lifespan function FastAPI uses this to run code before your app starts serving requests (setup), and after the app is shutting down (teardown).
So, the @asynccontextmanager lets you define this kind of "before and after" behavior in an async way.

SQLModel is an ORM (Object-Relational Mapper). It lets you define your database tables as Python classes (“models”), and then translates your Python code into SQL statements the database can understand.

Go beyond CRUD-
Alembic is a lightweight database migration tool , It helps you track, manage, and apply changes to your database schema over time, like adding new tables, columns, indexes, etc.
So u want to add a table but dont want to loose any previous data in the databse then we also use alembic
pip install alembic
alembic init -t async alembic_migrations
Then go to env.py under alembic and import which models u have created and also add target_metadata = SQLModel.metadata and  also add the db url , config.set_main_option('sqlalchemy.url', database_url)
and in the script.py.mako import sqlmodel.
alembic revision --autogenerate -m "init"
Then in the versions u can see a version and also u can see which table it will create in the upgrade func and now we can apply that migration so that table is created in our db
alembic upgrade head

Next is user account creation.