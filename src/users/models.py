from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from config.database.orm import Base
from users.password import is_bcrypt_pattern


class User(Base):
    __tablename__ = "service_user"

    id = Column(Integer, primary_key=True)
    username = Column(String(16), nullable=False)
    password = Column(String(60), nullable=False)  # bcrypt 최대 60자
    profile_image = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @classmethod
    def create(cls, username: str, password: str):
        assert is_bcrypt_pattern(password=password), "Invalid password pattern"
        return cls(username=username, password=password)

    def update_password(self, password: str) -> None:
        assert is_bcrypt_pattern(password=password), "Invalid password pattern"
        self.password = password
