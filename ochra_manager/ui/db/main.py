from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
import os


Base = declarative_base()


# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")  # Default to SQLite if not set

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("SESSION CREATED")

def init_db():
    print("Create all tables in the database.")
    inspector = inspect(engine)
    if not inspector.has_table('your_table_name'):  # You should specify a table name here
        Base.metadata.create_all(bind=engine)
    else:
        print("Tables already exist, skipping creation.")

def get_db():
    """Dependency for accessing the database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
