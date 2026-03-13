from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Поиск пользователя по email"""
        # формируем тело запроса в бд
        query = select(User).where(User.email == email)
        # асинхронно отправляем запрос в базу
        result = await self.session.execute(query)
        # и учитывая уникальность мыла, мы можем вернуть одного или никого - юзера
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Поиск пользователя по ID"""
        # здесь всё то же самое по сути делаем
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Добавление нового пользователя в базу"""
        # аля добавили объект юезра в нашу сессию
        self.session.add(user)
        # и уже здесь делаем sql запрос на создание
        await self.session.commit()
        # и теперь достаём айдишник свежего обьекта
        await self.session.refresh(user)
        return user