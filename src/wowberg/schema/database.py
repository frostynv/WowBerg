
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

# Read database configuration from environment variables
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "wowberg")
db_user = os.getenv("DB_USER", "wowberg")
db_password = os.getenv("DB_PASSWORD", "wowberg")

# Build database URL
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

# Shared declarative base for all models
class Base(DeclarativeBase):
    pass

class JsonSerializable:
    def to_dict(self) -> dict:
        """Convert SQLAlchemy model instance to a dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_json(self) -> str:
        """Convert the model instance to a JSON string."""
        import json
        return json.dumps(self.to_dict())

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """Create all tables defined in the models."""
    Base.metadata.create_all(bind=engine)