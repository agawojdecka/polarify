from typing import cast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import Base, engine, get_db
from app.api.schema.user import User as UserResponse
from app.domain.user import User as UserDomain
from app.repository import user as user_repo

router = APIRouter()
Base.metadata.create_all(bind=engine)


@router.get("/users/me", response_model=UserResponse)
def read_user(
    db: Session = Depends(get_db), current_user: UserDomain = Depends(get_current_user)
) -> UserResponse:
    db_user = user_repo.get_user(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = UserResponse(
        username=cast(str, db_user.username),
        email=cast(str, db_user.email),
    )
    return user
