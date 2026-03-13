from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

# Указываем FastAPI, где брать токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 1. Получение сессии БД
async def get_db():
    # я не много почитал и понял, что это очень крутая реализация
    # мы по сути используем контексный менеджр, который всегда закроет соединение
    # и мы используем yield как генератор, потому-что мы таким образом 
    # можем запомнить, где остановилась функция и пойти после дальше
    # и оказывается, что ранние генераторы, были по сути прототипами корутин)))
    async with AsyncSessionLocal() as session:
        yield session

# Очень красиво
# 1. получаем сессию с бд
# 2. создаём класс бизнес логики для управления пользователями
# 3. создаём класс для управления бд в этой логике и закидываем туда ещё сессию
# только меня тревожит, что мы по сути при каждом запросе будем создавать объекты
# мне страшно, что garbage collector может засориться. А вы что думаете?
async def get_auth_usecase(session: AsyncSession = Depends(get_db)):
    return AuthUseCase(UserRepository(session))


async def get_chat_usecase(session: AsyncSession = Depends(get_db)):
    return ChatUseCase(ChatMessageRepository(session), OpenRouterClient())

# Получение ID текущего пользователя из JWT
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен.")
        return int(user_id_str)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не получается проверить данные.")