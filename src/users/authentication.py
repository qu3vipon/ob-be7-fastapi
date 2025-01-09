import time
from typing import TypedDict

import jwt

from fastapi import Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from users.exceptions import JWTExpiredException, InvalidJWTException

class JWTPayload(TypedDict):
    user_id: int
    isa: float


JWT_SECRET_KEY = "9bb7bce418aad2ea4b6959515782f50d53541720e0bde5c17a9bc4da6d48c4eb"
JWT_ALGORITHM = "HS256"

# 1. 로그인 성공한 유저에게 access_token 발급
def create_access_token(user_id: int) -> str:
    payload: JWTPayload = {"user_id": user_id, "isa": time.time()}
    access_token: str = jwt.encode(
        payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return access_token


# 2. access_token 검증 & payload 반환
def verify_access_token(access_token: str) -> int:
    try:
        payload: JWTPayload = jwt.decode(
            jwt=access_token,
            key=JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except InvalidTokenError:
        raise InvalidJWTException

    issued_at: float = payload.get("isa", 0)
    if issued_at + (60 * 60 * 24 * 7) < time.time():
        raise JWTExpiredException

    return payload["user_id"]


bearer_auth = HTTPBearer()

def authenticate(auth_header: HTTPAuthorizationCredentials = Depends(bearer_auth)):
    access_token: str = auth_header.credentials
    user_id: int = verify_access_token(access_token=access_token)
    return user_id
