from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, UnauthorizedError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserPublic)
async def register(data: RegisterRequest, auth_service: AuthUseCase = Depends(get_auth_usecase)):
    try:
        return await auth_service.register_user(data)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthUseCase = Depends(get_auth_usecase)):
    try:
        token = await auth_service.login_for_token(form_data.username, form_data.password)
        return TokenResponse(access_token=token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserPublic)
async def get_me(user_id: int = Depends(get_current_user_id),auth_service: AuthUseCase = Depends(get_auth_usecase)):
    return await auth_service.get_user_profile(user_id)