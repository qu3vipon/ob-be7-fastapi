import bcrypt


def hash_password(plain_text: str) -> str:
    b_plain_text: bytes = plain_text.encode('utf-8')
    b_hashed_password: bytes = bcrypt.hashpw(b_plain_text, bcrypt.gensalt())
    return b_hashed_password.decode('utf-8')

def check_password(plain_text: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_text.encode('utf-8'),  # 사용자로부터 넘겨 받은 평문
        hashed_password.encode('utf-8')  # 서버에 보관 중인 비밀번호 해시 값
    )
