from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

from .config import get_settings

engine = create_engine(get_settings().db_url , echo=True)

Session = sessionmaker()

Base = declarative_base()