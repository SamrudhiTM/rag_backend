from app.models.user import User
from app.schemas.user import UserSignup, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status


async def signup_user(user_data: UserSignup) -> str:
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed = hash_password(user_data.password)

    new_user = User(email=user_data.email, hashed_password=hashed)
    await new_user.insert()

    token = create_access_token({"sub": str(new_user.id)})
    return token


async def login_user(user_data: UserLogin) -> str:
    user = await User.find_one(User.email == user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": str(user.id)})
    return token