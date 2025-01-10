from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends

from config.database.connection import get_db
from users.models import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()

    def get_users(self) -> list[User]:
        result = self.db.execute(select(User))
        return result.scalars().all()  # noqa

    def get_user_by_username(self, username: str) -> User | None:
        result = self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    def get_user_by_id(self, user_id: int) -> User | None:
        result = self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
