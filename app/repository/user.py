from datetime import datetime
from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.user import User, UserAuth
from app.models.user import User as UserModel


def get_user(db: Session, user_id: int) -> User | None:
    db_user = db.query(UserModel).filter_by(id=user_id).first()
    if not db_user:
        return None

    user = User(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at,
    )
    return user


def get_user_auth(db: Session, email: str) -> UserAuth | None:
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if not db_user:
        return None

    user = UserAuth(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at,
        password_hash=db_user.password_hash,
    )
    return user


def create_user(db: Session, *, email: str, username: str, password_hash: str) -> User:
    db_user = UserModel(username=username, email=email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    user = User(
        id=cast(int, db_user.id),
        username=username,
        email=email,
        created_at=cast(datetime, db_user.created_at),
    )
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if not db_user:
        return None

    user = User(
        id=db_user.id,
        username=db_user.username,
        email=email,
        created_at=db_user.created_at,
    )
    return user


def is_email_or_login_taken(db: Session, *, email: str, username: str) -> bool:
    stmt = (
        select(UserModel.id)
        .where((UserModel.email == email) | (UserModel.username == username))
        .limit(1)
    )
    result = db.execute(stmt).scalar_one_or_none()
    is_taken = result is not None

    return is_taken
