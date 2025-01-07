import os
import shutil
import uuid
from datetime import date

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import FileResponse

from users.exceptions import UserNotFoundException, UserProfileImgNotFoundException
from users.request import UserCreateRequestBody, UserUpdateRequestBody
from users.response import UserResponse, UserListResponse

router = APIRouter(tags=["Users"])

users = [
    {"id": 1, "name": "Elon Musk", "date_of_birth": date(1970, 1, 1), "image": "03ffd118-248f-46c9-a6df-3e90dd01c649_pizza.jpeg"},
    {"id": 2, "name": "Melon Musk", "date_of_birth": date(2000, 1, 1)},
]

# R: 전체 유저 목록 조회 API
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=UserListResponse,
)
def get_users_handler():
    return UserListResponse.model_validate({"users": users})


# C: 새로운 유저 생성 API
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def create_user_handler(body: UserCreateRequestBody):
    new_user = {
        "id": len(users) + 1,
        "name": body.name,
        "date_of_birth": body.date_of_birth,
    }
    users.append(new_user)
    return UserResponse.model_validate(new_user)

# R: 상세 유저 조회 API
@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def get_user_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return UserResponse.model_validate(user)
    raise UserNotFoundException

# U: 유저 업데이트 API
@router.patch(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def update_user_handler(user_id: int, body: UserUpdateRequestBody):
    for user in users:
        if user["id"] == user_id:
            user["name"] = body.name
            return UserResponse.model_validate(user)
    raise UserNotFoundException


# C: 사용자 프로필 이미지 업로드 API
@router.post(
    "/users/{user_id}/images",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def update_profile_image_handler(user_id: int, profile_image: UploadFile):
    for user in users:
        if user["id"] == user_id:
            unique_filename = f"{uuid.uuid4()}_{profile_image.filename}"
            file_path = os.path.join("users/images", unique_filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(profile_image.file, f)

            user["image"] = unique_filename
            return UserResponse.model_validate(user)
    raise UserNotFoundException

# R: 이미지 다운로드 API
@router.get(
    "/users/{user_id}/images/download",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def download_profile_image_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            if image := user.get("image"):
                file_path = os.path.join("users/images", image)
                original_filename = "".join(file_path.split("_")[1:])
                return FileResponse(
                    file_path,
                    headers={"Content-Disposition": f"attachment; filename={original_filename}"},
                )
            raise UserProfileImgNotFoundException
    raise UserNotFoundException

# D: 유저 삭제 API
@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_user_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
    raise UserNotFoundException
