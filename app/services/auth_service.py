from app.database import users_collection
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import UserSignup, UserLogin
from fastapi import HTTPException, status


async def signup_user(user_data: UserSignup) -> str:
    # Check if a user with this email already exists
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password before storing
    hashed = hash_password(user_data.password)

    # Insert the new user document into MongoDB
    new_user = {
        "email": user_data.email,
        "hashed_password": hashed,
    }
    await users_collection.insert_one(new_user)

    # Issue a token immediately so they're logged in right after signup
    token = create_access_token({"sub": user_data.email})
    return token


async def login_user(user_data: UserLogin) -> str:
    # Find the user by email
    user = await users_collection.find_one({"email": user_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify the password matches the stored hash
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Issue a token
    token = create_access_token({"sub": user_data.email})
    return token