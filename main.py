from fastapi import FastAPI
from src.database import Base, engine

# ИМПОРТ ВСЕХ МОДЕЛЕЙ (Обязательно!)
# Это те самые 4 структуры, о которых вы говорили
from src.auth.models import User      # Юзер (7 элементов)
from src.teams.models import Team     # Тим (3 элемента)
from src.products.models import Project # Проекты (4 элемента)
from src.events.models import Event    # Эвенты (5 элементов)

# Команда для создания таблиц
# Она пробегает по всем импортированным моделям и создает их в sql_app.db
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение роутеров для каждой структуры
# app.include_router(user_router)
# app.include_router(team_router)
# app.include_router(project_router)
# app.include_router(event_router)

@app.get("/")
def read_root():
    return {"message": "Таблицы успешно созданы, сервер запущен"}