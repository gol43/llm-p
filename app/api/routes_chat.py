from fastapi import APIRouter, Depends

from app.api.deps import get_chat_usecase, get_current_user_id
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def ask_llm(data: ChatRequest,
                  user_id: int = Depends(get_current_user_id),
                  chat_service: ChatUseCase = Depends(get_chat_usecase)):
    answer = await chat_service.ask_llm(user_id, data)
    return ChatResponse(answer=answer)


@router.get("/history")
async def get_history(user_id: int = Depends(get_current_user_id),
                      chat_service: ChatUseCase = Depends(get_chat_usecase)):
    return await chat_service.get_user_chat_history(user_id)


@router.delete("/history")
async def clear_history(user_id: int = Depends(get_current_user_id),
                        chat_service: ChatUseCase = Depends(get_chat_usecase)):
    await chat_service.clear_user_history(user_id)
    return {"message": "History cleared"}