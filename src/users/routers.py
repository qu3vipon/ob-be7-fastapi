from fastapi import APIRouter, UploadFile, Depends, status, Body, File
from fastapi.responses import FileResponse
from fastapi.security.http import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.exc import IntegrityError

from users.authentication import create_access_token, authenticate
from users.exceptions import UserNotFoundException, UserProfileImgNotFoundException, UserIncorrectPasswordException, \
    DuplicateUsernameException
from users.models import User
from users.password import hash_password, check_password
from users.repository import UserRepository
from users.request import UserCreateRequestBody, UserUpdateRequestBody
from users.response import UserResponse, UserListResponse, UserMeResponse, JWTResponse

basic_auth = HTTPBasic()

router = APIRouter(tags=["Users"])

# R: 전체 유저 목록 조회 API
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=UserListResponse,
)
def get_users_handler(
    _: int = Depends(authenticate),
    user_repo: UserRepository = Depends(),
):
    users = user_repo.get_users()
    return UserListResponse.model_validate({"users": users})


# C: 새로운 유저 생성 API
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserMeResponse,
)
def create_user_handler(
    body: UserCreateRequestBody,
    user_repo: UserRepository = Depends(),
):
    if user_repo.get_user_by_username(username=body.username):
        raise DuplicateUsernameException

    new_user = User.create(username=body.username, password=hash_password(plain_text=body.password))
    try:
        user_repo.save(user=new_user)
    except IntegrityError:
        raise DuplicateUsernameException
    return UserMeResponse.model_validate(new_user)


# R: 로그인 API
@router.get(
    "/users/login",
    status_code=status.HTTP_200_OK,
)
def user_login_handler(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
    user_repo: UserRepository = Depends(),
):
    if not (user := user_repo.get_user_by_username(username=credentials.username)):
        raise UserNotFoundException
    if not check_password(plain_text=credentials.password, hashed_password=user.password):
        raise UserIncorrectPasswordException
    return JWTResponse(access_token=create_access_token(user_id=user.id))


# R: 내 정보 조회 API
@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeResponse,
)
def get_me_handler(
    me_id: int = Depends(authenticate),
    user_repo: UserRepository = Depends(),
):
    if not (user := user_repo.get_user_by_id(user_id=me_id)):
        raise UserNotFoundException
    return UserMeResponse.model_validate(user)


# R: 유저 상세 조회 API
@router.get(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
def get_user_handler(
    user_id: int,
    user_repo: UserRepository = Depends(),
):
    if not (user := user_repo.get_user_by_id(user_id=user_id)):
        raise UserNotFoundException
    return UserResponse.model_validate(user)

# U: 유저 업데이트 API
@router.patch(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=UserMeResponse,
)
def update_user_handler(
    me_id: int = Depends(authenticate),
    body: UserUpdateRequestBody = Body(),
    user_repo: UserRepository = Depends(),
):
    if not (user := user_repo.get_user_by_id(user_id=me_id)):
        raise UserNotFoundException

    user.update_password(password=hash_password(plain_text=body.password))
    user_repo.save(user=user)
    return UserMeResponse.model_validate(user)


# C: 사용자 프로필 이미지 업로드 API
@router.post(
    "/users/me/images",
    status_code=status.HTTP_201_CREATED,
    response_model=UserMeResponse,
)
def upload_profile_image_handler(
    user_id: int = Depends(authenticate),
    profile_image: UploadFile = File(),
    user_repo: UserRepository = Depends(),
):
    if not (user := user_repo.get_user_by_id(user_id=user_id)):
        raise UserNotFoundException

    user.upload_profile_image(profile_image=profile_image)
    user_repo.save(user=user)
    return UserMeResponse.model_validate(user)


# R: 이미지 다운로드 API
@router.get(
    "/users/{user_id}/images",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def download_profile_image_handler(
    user_id: int,
    _: int = Depends(authenticate),
    user_repo: UserRepository = Depends(),
):
    if not (user := user_repo.get_user_by_id(user_id=user_id)):
        raise UserNotFoundException
    if not user.profile_image:
        raise UserProfileImgNotFoundException
    return FileResponse(user.profile_image)



# D: 유저 삭제 API
@router.delete(
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_user_handler(
    user_id: int = Depends(authenticate),
    user_repo: UserRepository = Depends(),
):
    if not (user := user_repo.get_user_by_id(user_id=user_id)):
        raise UserNotFoundException

    user_repo.delete(user=user)
