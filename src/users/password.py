import bcrypt


def hash_password(plain_text: str) -> str:
    plain_text_bytes: bytes = plain_text.encode('utf-8')
    hashed_password_bytes: bytes = bcrypt.hashpw(plain_text_bytes, bcrypt.gensalt())
    return hashed_password_bytes.decode('utf-8')

def check_password(plain_text: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_text.encode('utf-8'),  # 사용자로부터 넘겨 받은 평문
        hashed_password.encode('utf-8')  # 서버에 보관 중인 비밀번호 해시 값
    )
