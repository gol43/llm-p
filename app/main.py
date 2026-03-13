import uvicorn
from fastapi import FastAPI

from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router
from app.db.base import Base
from app.db.session import engine


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def create_app() -> FastAPI:
    app = FastAPI(title="Protected-API-for-llm-Saygushev_M25-555")

    app.include_router(auth_router)
    app.include_router(chat_router)

    @app.on_event("startup")
    async def on_startup():
        await create_tables()

    @app.get("/health")
    async def health():
        return {"status": "ok", "environment": "local"}

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)