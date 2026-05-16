from pydantic import BaseModel
from pydantic import EmailStr


class UserRegister(BaseModel):

    username: str

    email: EmailStr

    password: str


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"