import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL

    async def get_completion(self, messages: list[dict], temperature: float = 1.0) -> str:
        """Отправка запроса в OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=10) # чтобы бесконечно не висел запрос, если чёт залагало)
                
                if response.status_code != 200:
                    raise ExternalServiceError(f"OpenRouter ошибка: {response.text}")
                
                result = response.json()
                return result["choices"][0]["message"]["content"]

            except httpx.RequestError as exc:
                raise ExternalServiceError(f"Ошибка внешнего сервиса OpenRouter: {exc}")