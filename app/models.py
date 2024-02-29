from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from .db import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    target_url = Column(String)
    key = Column(String , unique = True)
    admin_key = Column(String, unique=True)
    is_active = Column(Boolean) 
    clicks = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())