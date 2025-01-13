import os
import shutil
import uuid
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

from config.database.orm import Base
from users.password import is_bcrypt_pattern


class User(Base):
    __tablename__ = "service_user"

    id = Column(Integer, primary_key=True)
    username = Column(String(16), nullable=False)
    password = Column(String(60), nullable=False)  # bcrypt 최대 60자
    profile_image = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    __table_args__ = (
        UniqueConstraint("username", name="uix_service_user_username"),
    )

    @classmethod
    def create(cls, username: str, password: str):
        assert is_bcrypt_pattern(password=password), "Invalid password pattern"
        return cls(username=username, password=password)

    def update_password(self, password: str) -> None:
        assert is_bcrypt_pattern(password=password), "Invalid password pattern"
        self.password = password

    def remove_profile_image(self) -> None:
        if self.profile_image:
            os.remove(self.profile_image)

    def upload_profile_image(self, profile_image: UploadFile):
        self.remove_profile_image()

        unique_filename: str = f"{uuid.uuid4()}_{profile_image.filename}"
        file_path: str = os.path.join("users/images", unique_filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(profile_image.file, f)

        self.profile_image = file_path
