import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.token import AuthToken
from app.repository.user import get_user


@dataclass
class AuthTokenData:
    user_id: int
    token: str


@dataclass
class UserNotFoundException(Exception):
    pass


def create_auth_token(db: Session, user_id: int) -> AuthTokenData:
    user = get_user(db, user_id)
    if not user:
        raise UserNotFoundException

    token = uuid.uuid4().hex
    auth_token = AuthToken(user_id=user.id, token=token)
    db.add(auth_token)
    db.commit()
    db.refresh(auth_token)

    auth_token_data = AuthTokenData(
        user_id=auth_token.user_id,
        token=auth_token.token,
    )
    return auth_token_data


def get_auth_token(db: Session, user_id: int) -> AuthTokenData | None:
    db_auth_token = db.query(AuthToken).filter(AuthToken.user_id == user_id).first()
    if not db_auth_token:
        return None

    auth_token_data = AuthTokenData(user_id=user_id, token=db_auth_token.token)
    return auth_token_data
