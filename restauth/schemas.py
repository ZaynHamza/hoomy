from ninja import Schema
from pydantic import EmailStr, Field


class AccountIn(Schema):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    profile_pic: str = None


class TokenOut(Schema):
    access: str


class AccountOut(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    profile_pic: str = None


class AuthOut(Schema):
    token: TokenOut
    account: AccountOut


class SigninIn(Schema):
    email: EmailStr
    password: str
