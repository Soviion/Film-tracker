from app.database import Base, engine
from app.models import User, WatchedItem

print("Подключаемся к базе данных...")
print("DATABASE_URL из .env:", engine.url)  # Покажет, к какой базе пытаемся подключиться

try:
    print("Создаём таблицы...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")
    print("\nСозданы таблицы:")
    print("- users")
    print("- watched_items")
except Exception as e:
    print("ОШИБКА при создании таблиц:")
    print(e)