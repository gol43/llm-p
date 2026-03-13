from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublic(BaseModel):
    """Публичная информация о пользователе."""
    
    id: int
    email: EmailStr
    role: str
    
    # чтобы FastAPI мог возвращать ORM-объекты напрямую как схему
    model_config = ConfigDict(from_attributes=True)