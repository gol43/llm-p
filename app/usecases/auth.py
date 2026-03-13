from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, data: RegisterRequest) -> User:
        """Регистрация"""
        # Проверяем, не занят ли email
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise ConflictError(f"Пользователь с таким email {data.email} уже существует!")
        # По сути нужно бы ещё ввести проверку, что пользователь не должен быть залогинен ещё 
        
        # Вопрос к ревьюверу!!!!!!!!!!: где, по законам чистой архитектуры, мы должны создавать объект юзера?
        # в бизнес-логике или в репозитории?
        # Мы ведь если запихнём это в репозиторий, то так даже лучше будет работать инверсия зависимостей.
        # Но при этом в ТЗ как-будто написано, что нужно делать тут)))
        new_user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            role="user"
        )
        
        # Делаем запрос в бд
        return await self.user_repo.create(new_user)

    async def login_for_token(self, email: str, password: str) -> str:
        """Логин"""
        # Ищем нашего пользователя
        user = await self.user_repo.get_by_email(email)
        
        # Если пользователя нет или пароль не подходит, то GG
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Неверные данные! Проверьте логин и пароль.")

        # Генерируем токен
        token_data = {"sub": str(user.id), "role": user.role}
        return create_access_token(token_data)

    async def get_user_profile(self, user_id: int) -> User:
        """Получение данных профиля"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("Пользователь не найден.")
        return user