from datetime import date

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str


class UserListResponse(BaseModel):
    users: list[UserResponse]


class UserMeResponse(BaseModel):
    id: int
    username: str
    password: str


class JWTResponse(BaseModel):
    access_token: str
