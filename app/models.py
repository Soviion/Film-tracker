from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

    watched_items = relationship("WatchedItem", back_populates="user")

class WatchedItem(Base):
    __tablename__ = "watched_items"

    id = Column(Integer, primary_key=True, index=True)
    imdb_id = Column(String, unique=True, nullable=False)  # Уникальный IMDb ID
    title = Column(String, nullable=False)
    year = Column(String)
    media_type = Column(String, nullable=False)  # "movie" или "tv"
    poster_url = Column(String)
    personal_rating = Column(Float)  # 0.0 - 10.0
    status = Column(String, default="planned")  # planned, watching, completed, dropped
    notes = Column(String)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_completed = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="watched_items")