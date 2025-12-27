from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WatchedItemBase(BaseModel):
    imdb_id: str
    title: str
    year: Optional[str] = None
    media_type: str  # movie или tv
    poster_url: Optional[str] = None

class WatchedItemCreate(WatchedItemBase):
    status: Optional[str] = "planned"
    personal_rating: Optional[float] = None
    notes: Optional[str] = None

class WatchedItemResponse(WatchedItemBase):
    id: int
    status: str
    personal_rating: Optional[float]
    notes: Optional[str]
    date_added: datetime
    date_completed: Optional[datetime]

    class Config:
        from_attributes = True