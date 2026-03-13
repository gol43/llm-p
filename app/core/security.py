from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Мы используем алгоритм bcrypt, который является "золотым стандартом".
# В уроках вроде бы было написано, что он специально сделан медленным, 
# чтобы защитить от перебора (brute-force).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Превращает "сырой" пароль в хеш, чтобы не хранить пароль в БД в сыром виде"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли введенный пароль сохраненному хешу. 
    Мы тут по сути не расшифровываем хеш, а заново хешируем ввод и сравниваем результаты."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Генерация JWT access token"""
    to_encode = data.copy()
    
    # Устанавливаем срок действия токена
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_access_token(token: str) -> dict:
    """Декодирует токен и проверяет его подпись"""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])