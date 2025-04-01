from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
import secrets

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False, default=lambda: secrets.token_hex(16))
    github_pat = Column(String, nullable=True)  # optional, can be null initially
    request_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
