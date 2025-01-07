from datetime import date

from pydantic.main import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    date_of_birth: date
    image: str = ""


class UserListResponse(BaseModel):
    users: list[UserResponse]
