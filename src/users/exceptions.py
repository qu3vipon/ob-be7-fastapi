from fastapi import status, HTTPException

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

UserProfileImgNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User profile image not found"
)

UserIncorrectPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)

InvalidJWTException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid JWT",
)

JWTExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="JWT expired",
)

DuplicateUsernameException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already exists",
)
