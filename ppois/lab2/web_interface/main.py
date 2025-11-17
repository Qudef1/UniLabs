from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database import SessionLocal, engine
from models import User, Base

# Создаём таблицы в БД (если их ещё нет)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Зависимость: получаем сессию БД для каждого запроса
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Хеширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Модели данных (для запроса и ответа)
class UserCreate(BaseModel):
    username: str
    email: EmailStr  # Автоматическая валидация email
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Раньше называлось orm_mode = True

# Роут регистрации
@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка: существует ли уже такой email или username
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email или именем уже существует"
        )

    # Хешируем пароль
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)

    # Создаём объект пользователя
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    # Сохраняем в БД
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Получаем id из БД

    return db_user