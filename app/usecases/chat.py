from app.repositories.chat_messages import ChatMessageRepository
from app.schemas.chat import ChatRequest
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self, chat_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self.chat_repo = chat_repo
        self.llm_client = llm_client

    async def ask_llm(self, user_id: int, chat_data: ChatRequest) -> str:
        """Логика нашего общения с ИИ"""
        
        # Собираем список сообщений для модели
        messages_for_llm = []

        # Добавляем системную инструкцию, если она есть
        if chat_data.system:
            messages_for_llm.append({"role": "system", "content": chat_data.system})

        # Достаём историю общения для контекста
        history = await self.chat_repo.get_history(user_id, limit=chat_data.max_history)
        # Я даже не знаю, это конеш заблокирует нам event loop, но иначе не знаю как сделать((
        for msg in history:
            messages_for_llm.append({"role": msg.role, "content": msg.content})

        # Добавлявем текущий промпт
        messages_for_llm.append({"role": "user", "content": chat_data.prompt})

        # И обновляем историю бд
        await self.chat_repo.add_message(user_id, "user", chat_data.prompt)

        # Core функция, которая непосредственно и делает запрос к ИИ
        answer = await self.llm_client.get_completion(messages=messages_for_llm, temperature=chat_data.temperature)

        # Сохраняем ответ ИИ в базу данных
        # OpenRouter ошибка: {"error":{"message":"Provider returned error","code":400,"metadata":{"raw":"{\"error\":{\"message\":\"invalid msg role: llm-bot\",\"type\":\"request_params_invalid\"}}","provider_name":"StepFun","is_byok":false}},"user_id":"user_30ySQG3jDpxOfhohmImFMXcmCJG"}
        # нужно писать о таком в ТЗ, что нужно роль особую задавать!
        await self.chat_repo.add_message(user_id, "assistant", answer)

        return answer

    async def get_user_chat_history(self, user_id: int):
        """Получение истории общения"""
        return await self.chat_repo.get_history(user_id, limit=100)

    async def clear_user_history(self, user_id: int):
        """Очистука истории общения"""
        await self.chat_repo.clear_history(user_id)