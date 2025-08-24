import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Environment variable (from .env or Docker)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
