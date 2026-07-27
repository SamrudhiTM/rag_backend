from fastapi import APIRouter
from app.models.user import UserSignup, UserLogin, TokenResponse
from app.services.auth_service import signup_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup):
    token = await signup_user(user_data)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    token = await login_user(user_data)
    return TokenResponse(access_token=token)