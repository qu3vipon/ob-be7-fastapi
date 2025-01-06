import os
import shutil
import uuid
from datetime import date

from fastapi import APIRouter, UploadFile

from users.request import UserCreateRequestBody, UserUpdateRequestBody

router = APIRouter(tags=["Users"])

users = [
    {"id": 1, "name": "Elon Musk", "date_of_birth": date(1970, 1, 1)},
    {"id": 2, "name": "Melon Musk", "date_of_birth": date(2000, 1, 1)},
]

# 전체 유저 목록 조회 API
@router.get("/users")
def get_users_handler():
    return users

# C: 새로운 유저 생성 API
@router.post("/users")
def create_user_handler(body: UserCreateRequestBody):
    # 1. 사용자로부터 데이터를 받고
    # 2. 받은 데이터의 유효성 검사

    # 3. 새로운 유저 데이터를 유저 목록 추가
    new_user = {
        "id": len(users) + 1,
        "name": body.name,
        "date_of_birth": body.date_of_birth,
    }
    users.append(new_user)
    return new_user

# R: 상세 유저 조회 API
@router.get("/users/{user_id}")
def get_user_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

# U: 유저 업데이트 API
@router.patch("/users/{user_id}")
def update_user_handler(user_id: int, body: UserUpdateRequestBody):
    for user in users:
        if user["id"] == user_id:
            user["name"] = body.name
            return user

# U: 사용자 프로필 이미지 업데이트 API
@router.post("/users/{user_id}/images")
def update_profile_image_handler(user_id: int, profile_image: UploadFile):
    for user in users:
        if user["id"] == user_id:
            unique_filename = f"{uuid.uuid4()}_{profile_image.filename}"
            file_path = os.path.join("users/images", unique_filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(profile_image.file, f)

            user["image"] = unique_filename
            return user

# D: 유저 삭제 API
@router.delete("/users/{user_id}")
def delete_user_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
    return users
