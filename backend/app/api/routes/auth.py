from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user import User

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse
)

from app.schemas.user import (
    UserResponse
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# REGISTER
# ==========================================

@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # Check existing email
    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check existing username
    existing_username = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create user
    new_user = User(

        username=user_data.username,

        email=user_data.email,

        hashed_password=hash_password(
            user_data.password
        )
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# ==========================================
# LOGIN
# ==========================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token({

        "sub": user.id
    })

    return {

        "access_token": access_token,

        "token_type": "bearer"
    }

