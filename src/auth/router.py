from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload

from src.database import get_db
from src.auth.models import User
# Импортируем обе схемы: для регистрации и для логина
from src.auth.schemas import UserRegisterSchema, UserLoginSchema 

# 1. Инициализация объектов (обязательно в начале файла)
config = AuthXConfig(
    JWT_SECRET_KEY="test-secret-key",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)
security = HTTPBearer()

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# 2. API Регистрации (создает пользователя и возвращает 2 токена)
@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserRegisterSchema,    
    db: Session = Depends(get_db)
):
    # Проверка уникальности email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )

    new_user = User(
        email=user_data.email,
        password=user_data.password, # В реальном проекте используй хеширование!
        first_name="",          
        last_name=""
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)              

    # Создаем сразу два токена
    access_token = auth.create_access_token(uid=new_user.email)
    refresh_token = auth.create_refresh_token(uid=new_user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "Регистрация прошла успешно"
    }

# 3. API Логина (принимает JSON в теле запроса)
@user_router.post("/login")
def login(
    user_data: UserLoginSchema, # Теперь данные идут через Body, а не через URL
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or user.password != user_data.password:
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль"
        )

    # Создаем сразу два токена
    access_token = auth.create_access_token(uid=user.email)
    refresh_token = auth.create_refresh_token(uid=user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# 4. API Refresh (принимает Refresh Token и проверяет его по дате)
@user_router.post("/refresh")
def refresh(
    payload: TokenPayload = Depends(auth.refresh_token_required),
    credentials = Depends(security)
):
    """
    Библиотека AuthX сама декодирует токен и проверяет его срок годности (exp).
    Если дата истекла, вернется ошибка 401.
    """
    # Генерируем новые токены на основе данных из старого (payload.sub)
    new_access_token = auth.create_access_token(uid=payload.sub)
    new_refresh_token = auth.create_refresh_token(uid=payload.sub)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# 5. Защищенный API (проверка Access Token)
@user_router.get("/protected")
def protected(
    payload: TokenPayload = Depends(auth.access_token_required),
    credentials = Depends(security)
):
    return {"message": f"Доступ разрешен для: {payload.sub}"}