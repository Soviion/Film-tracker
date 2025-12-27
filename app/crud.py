from sqlalchemy.orm import Session
from .models import WatchedItem
from .schemas import WatchedItemCreate

def create_watched_item(db: Session, item: WatchedItemCreate, user_id: int):
    # Проверяем, нет ли уже такого imdb_id у пользователя
    existing = db.query(WatchedItem).filter(
        WatchedItem.imdb_id == item.imdb_id,
        WatchedItem.user_id == user_id
    ).first()
    if existing:
        return None  # уже есть

    db_item = WatchedItem(
        **item.dict(),
        user_id=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_list(db: Session, user_id: int):
    return db.query(WatchedItem).filter(WatchedItem.user_id == user_id).all()