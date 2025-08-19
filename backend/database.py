from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the database URL. This points to a file named 'sql_app.db' in the same directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Create the SQLAlchemy engine. This is the core of the database connection.
# The 'connect_args' is needed only for SQLite to allow multi-threaded interaction.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class. Each instance of this class will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class. Our database model classes will inherit from this class.
Base = declarative_base()