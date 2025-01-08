from pydantic import BaseModel


class UserCreateRequestBody(BaseModel):
    username: str
    password: str


class UserUpdateRequestBody(BaseModel):
    name: str
