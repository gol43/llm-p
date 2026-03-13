from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

Password = Annotated[str, Field(min_length=4, max_length=16)] # достаточно элегенатно, хотя можно было и через Field

class RegisterRequest(BaseModel):
    """Данные для регистрации нового пользователя"""
    email: EmailStr
    password: Password 

class TokenResponse(BaseModel):
    """Формат ответа при логине"""
    access_token: str
    token_type: str = "bearer"