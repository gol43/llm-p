from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Сохранение нового сообщения"""
        # связываем для бд автора и сообщение
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_history(self, user_id: int, limit: int = 10) -> list[ChatMessage]:
        """Получение истории последних сообщений пользователя."""
        query = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id) 
            .order_by(ChatMessage.created_at.desc()) # сортировка
            .limit(limit) # N кол-во объектов
        )
        result = await self.session.execute(query)
        messages = result.scalars().all()
        # Возвращаем в хронологическом порядке
        return list(reversed(messages))

    async def clear_history(self, user_id: int) -> None:
        """Удаление всех сообщений конкретного пользователя"""
        query = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self.session.execute(query)
        await self.session.commit()