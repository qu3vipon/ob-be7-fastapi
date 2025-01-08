import time

import jwt

from users.exceptions import JWTExpiredException

JWT_SECRET_KEY = "9bb7bce418aad2ea4b6959515782f50d53541720e0bde5c17a9bc4da6d48c4eb"
JWT_ALGORITHM = "HS256"

# 1. 로그인 성공한 유저에게 access_token 발급
def create_access_token(user_id: int) -> str:
    payload = {"user_id": user_id, "isa": time.time()}
    access_token = jwt.encode(
        payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return access_token


# 2. access_token 검증 & payload 반환
def verify_access_token(access_token: str) -> int:
    payload = jwt.decode(
        token=access_token,
        key=JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )
    issued_at: float = payload.get("isa", 0)
    if issued_at + (60 * 60 * 24) < time.time():
        raise JWTExpiredException

    return payload["user_id"]
