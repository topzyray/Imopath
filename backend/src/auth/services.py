from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel, UserUpdateModel
from .model import User
from .utils import generate_password_hash, verify_password



class UserService:
    # Find user by email
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    # Find user by username
    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    # Checks if user exists
    async def user_exists(self, username: str, email: str, session: AsyncSession):
        user_by_username = await self.get_user_by_username(username, session)
        user_by_emal = await self.get_user_by_email(email, session)
        return True if user_by_username or user_by_emal is not None else False
    
    # Create new user if they do not exists
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        existing_user = await self.user_exists(user_data_dict["username"], user_data_dict["email"], session)

        if existing_user:
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"Choose another username or email")

        new_user = User(
            **user_data_dict
        )

        new_user.user_type = new_user.user_type.upper()
        new_user.password_hash = generate_password_hash(user_data_dict["password"])

        print(new_user)
        session.add(new_user)
        await session.commit()
        return new_user
    
    # # Find all the users in the database
    # async def get_all_users(self, session: AsyncSession):
    #     statement = select(User).order_by(desc(User.created_at))
    #     result = await session.exec(statement)
    #     return result.all()
    
    # # Find user by their unique id
    # async def get_user_by_id(self, user_uid: str, session: AsyncSession):
    #     statement = select(User).where(User.uid == user_uid)
    #     result = await session.exec(statement)
    #     user = result.first()
    #     return user if user is not None else None
    
    # # Update an existing user
    # async def update_user(self, user_uid: str, update_user_data: UserUpdateModel, session: AsyncSession):
    #     user_to_update = await self.get_user(user_uid, session)

    #     if user_to_update is not None:
    #         update_data_dict = update_user_data.model_dump()

    #         for k, v in update_data_dict.items():
    #             setattr(user_to_update, k, v)

    #         await session.commit()
    #         return user_to_update
    #     else:
    #         return None
        
    # # Delete a user by their id
    # async def delete_user(self, user_uid: str, session: AsyncSession):
    #     user_to_delete = await self.get_user_by_id(user_uid, session)

    #     if user_to_delete is not None:
    #         await session.delete(user_to_delete)
    #         await session.commit()
    #         return {}
    #     else:
    #         return None