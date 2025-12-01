from dataclasses import dataclass

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.repository import auth_token as auth_token_repo
from app.repository import user as user_repo

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


@dataclass
class RegisterUserInputData:
    username: str
    email: str
    password: str


@dataclass
class RegisterUserOutputData:
    token: str


class EmailOrUsernameTakenException(Exception):
    pass


def register_user(
    db: Session, register_user_input_data: RegisterUserInputData
) -> RegisterUserOutputData:
    is_email_or_login_taken = user_repo.is_email_or_login_taken(
        db,
        email=register_user_input_data.email,
        username=register_user_input_data.username,
    )
    if is_email_or_login_taken:
        raise EmailOrUsernameTakenException

    password_hash = pwd_context.hash(register_user_input_data.password)

    user = user_repo.create_user(
        db,
        email=register_user_input_data.email,
        username=register_user_input_data.username,
        password_hash=password_hash,
    )

    auth_token_data = auth_token_repo.create_auth_token(db, user_id=user.id)
    register_user_output_data = RegisterUserOutputData(token=auth_token_data.token)

    return register_user_output_data


@dataclass
class LoginUserInputData:
    email: str
    password: str


@dataclass
class LoginUserOutputData:
    id: int
    username: str
    email: str
    token: str


@dataclass
class IncorrectLoginDetailsException(Exception):
    pass


def login_user(
    db: Session, login_user_input_data: LoginUserInputData
) -> LoginUserOutputData:
    user_auth = user_repo.get_user_auth(db, login_user_input_data.email)
    if not user_auth:
        raise IncorrectLoginDetailsException

    is_password_verified = verify_password(
        login_user_input_data.password, user_auth.password_hash
    )
    if not is_password_verified:
        raise IncorrectLoginDetailsException

    auth_token_data = auth_token_repo.get_auth_token(db, user_id=user_auth.id)
    assert auth_token_data

    login_user_output_data = LoginUserOutputData(
        id=user_auth.id,
        username=user_auth.username,
        email=user_auth.email,
        token=auth_token_data.token,
    )

    return login_user_output_data


def verify_password(password: str, password_hash: str) -> bool:
    is_password_verified = pwd_context.verify(password, password_hash)
    return is_password_verified
