from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

DATABASE_URL = f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"


engine = create_async_engine(DATABASE_URL)
# для тестирования можно добавить echo=True, чтобы видет сырые sql запросы.

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False)

# expire_on_commit=False предотвращает протухание объектов после комита,
# позволяя нам обращаться к полям после сохранения.