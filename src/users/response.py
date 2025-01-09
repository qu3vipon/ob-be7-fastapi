from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: list[UserResponse]

    model_config = ConfigDict(from_attributes=True)


class UserMeResponse(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JWTResponse(BaseModel):
    access_token: str
