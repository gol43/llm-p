from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Запрос пользователя к ИИ"""
    prompt: str = Field(description="Основной текст запроса")
    system: Optional[str] = Field(None, description="Системная инструкция")
    max_history: int = Field(10, ge=1, le=50, description="Сколько сообщений брать из истории")
    
    # ExternalServiceError: OpenRouter ошибка: {"error":{"message":"Expected temperature to be at most 2, received 5","code":400,"metadata":{"provider_name":null}}}
    # Нужно в ТЗ писать о таких ограничениях АПИ!!!!
    temperature: float = Field(1.0, ge=0.0, le=2.0, description="Креативность модели")  

class ChatResponse(BaseModel):
    """Ответ от ИИ"""
    answer: str