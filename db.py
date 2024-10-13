from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL connection
db_url = "sqlite:///./globant_challenge.db"

# Create engine and session
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for table models
Base = declarative_base()

# Function to initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
