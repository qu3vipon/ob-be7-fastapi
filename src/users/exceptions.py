from fastapi import status, HTTPException

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

UserProfileImgNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User profile image not found"
)
