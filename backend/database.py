import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT as MediumText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Load environment variables
load_dotenv()

# --- Database Configuration (MySQL Example) ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# MySQL Database URL
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca=/etc/ssl/certs/ca.pem"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the Quiz Model (Remains the same)
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    date_generated = Column(DateTime, default=datetime.datetime.now)
    scraped_content = Column(MediumText)
    full_quiz_data = Column(Text, nullable=False)

def create_db_tables():
    """Creates all defined database tables if they do not already exist."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully or already exist.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise # Re-raise the exception to make errors clear

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This __name__ == "__main__" block is for manual testing/initial setup
if __name__ == "__main__":
    print("Attempting to connect to MySQL database and create tables...")
    create_db_tables()