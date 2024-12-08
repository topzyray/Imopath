from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.schemas import UserModel, UserCreateModel, UserLoginModel
from src.auth.services import UserService
from .utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    username = user_data.username

    user_exists = await user_service.user_exists(email, username, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email or username already exists")

    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'émail': user.email,
                    'user_uid': str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'émail': user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login successfull",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                       "email": user.email,
                       "uid": str(user.uid) 
                    }
                }
            )     
        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")




# @user_router.get("/", response_model=List[User])
# async def get_all_users(session: AsyncSession = Depends(get_session)):
#     users = await user_service.get_all_users(session)
#     return users


# @user_router.get("/{user_uid}", response_model=User)
# async def get_user(user_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
#     user = await user_service.get_user_by_id(user_uid, session)
    
#     if user:
#         return user
#     else:    
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User not found")


