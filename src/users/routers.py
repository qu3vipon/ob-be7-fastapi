import os
import shutil
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import FileResponse
from fastapi.security.http import HTTPBasic, HTTPBasicCredentials

from config.database.connection import SessionFactory, get_db
from users.authentication import create_access_token, authenticate
from users.exceptions import UserNotFoundException, UserProfileImgNotFoundException, UserIncorrectPasswordException
from users.models import User
from users.password import hash_password, check_password
from users.request import UserCreateRequestBody, UserUpdateRequestBody
from users.response import UserResponse, UserListResponse, UserMeResponse, JWTResponse

basic_auth = HTTPBasic()

router = APIRouter(tags=["Users"])

users = [
    {"id": 1, "username": "elon", "password": "$2b$12$5bOZcnA0C6Q/o2vQMs3.1eDCnoa9.G0X0JDYal7Y6kQh1700VKAG6"},
    {"id": 2, "username": "melon", "password": "$2b$12$ZkMKkONFhNytTkOK3M9r..I5mugNncSTf0ZwJlWWo3D7pLBHhEdcm"},
]

# R: 전체 유저 목록 조회 API
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=UserListResponse,
)
def get_users_handler(
    _: int = Depends(authenticate),
    db: Session = Depends(get_db),
):
    users_query = db.execute(select(User))
    users = users_query.scalars().all()
    return UserListResponse.model_validate({"users": users})


# C: 새로운 유저 생성 API
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserMeResponse,
)
def create_user_handler(
    body: UserCreateRequestBody,
    db: Session = Depends(get_db),
):
    new_user = User(username=body.username, password=hash_password(plain_text=body.password))
    db.add(new_user)
    db.commit()
    return UserMeResponse.model_validate(new_user)


# R: 로그인 API
@router.get(
    "/users/login",
    status_code=status.HTTP_200_OK,
)
def user_login_handler(credentials: HTTPBasicCredentials = Depends(basic_auth)):
    # Basic Auth 이용해서 Header로 Credentials -> 비밀번호 확인 -> access_token(JWT) 발급
    for user in users:
        if credentials.username == user["username"]:
            if check_password(plain_text=credentials.password, hashed_password=user["password"]):
                return JWTResponse(access_token=create_access_token(user_id=user["id"]))
            raise UserIncorrectPasswordException
    raise UserNotFoundException


# R: 내 정보 조회 API
@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeResponse,
)
def get_me_handler(user_id: int = Depends(authenticate)):
    for user in users:
        if user_id == user["id"]:
            return UserMeResponse.model_validate(user)
    raise UserNotFoundException


# R: 유저 상세 조회 API
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
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def update_user_handler(
    body: UserUpdateRequestBody,
    user_id: int = Depends(authenticate),
):
    for user in users:
        if user["id"] == user_id:
            user["username"] = body.username
            return UserResponse.model_validate(user)
    raise UserNotFoundException


# C: 사용자 프로필 이미지 업로드 API
@router.post(
    "/users/me/images",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
def update_profile_image_handler(
    profile_image: UploadFile,
    user_id: int = Depends(authenticate),
):
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
    "/users/me/images/download",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def download_profile_image_handler(user_id: int = Depends(authenticate)):
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
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_user_handler(user_id: int = Depends(authenticate)):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
    raise UserNotFoundException
