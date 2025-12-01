from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.domain.user import User as UserDomain
from app.models.token import AuthToken
from app.models.user import User as UserModel


async def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> UserDomain:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
    else:
        token = authorization

    auth = db.query(AuthToken).filter(AuthToken.token == token).first()

    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    db_user = db.query(UserModel).filter(UserModel.id == auth.user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not found",
        )

    current_user = UserDomain(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at,
    )

    return current_user
