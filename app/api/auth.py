from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.services.auth import (
    EmailOrUsernameTakenException,
    IncorrectLoginDetailsException,
    LoginUserInputData,
    RegisterUserInputData,
    login_user,
    register_user,
)

router = APIRouter()


class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class RegisterUserResponse(BaseModel):
    token: str


@router.post("/register/")
def registration(
    register_user_request: RegisterUserRequest, db: Session = Depends(get_db)
) -> RegisterUserResponse:
    register_user_input_data = RegisterUserInputData(
        username=register_user_request.username,
        email=str(register_user_request.email),
        password=register_user_request.password,
    )

    try:
        register_user_data = register_user(db, register_user_input_data)
    except EmailOrUsernameTakenException:
        raise HTTPException(
            status_code=400, detail="This email or username is already in use."
        )

    response = RegisterUserResponse(token=register_user_data.token)

    return response


class LoginUserRequest(BaseModel):
    email: str
    password: str


class LoginUserResponse(BaseModel):
    id: int
    username: str
    email: str
    token: str


@router.post("/login/")
def login(
    login_user_request: LoginUserRequest, db: Session = Depends(get_db)
) -> LoginUserResponse:
    login_user_input_data = LoginUserInputData(
        email=login_user_request.email,
        password=login_user_request.password,
    )

    try:
        login_user_output_data = login_user(db, login_user_input_data)
    except IncorrectLoginDetailsException:
        raise HTTPException(status_code=400, detail="Incorrect login details.")

    response = LoginUserResponse(
        id=login_user_output_data.id,
        username=login_user_output_data.username,
        email=login_user_output_data.email,
        token=login_user_output_data.token,
    )
    return response
