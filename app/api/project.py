from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.domain.user import User as UserDomain
from app.repository.project import (
    ProjectNotFoundException,
    create_project,
    delete_project,
    get_project,
    list_projects,
    update_project,
)

router = APIRouter()


class ProjectCreateUpdateRequest(BaseModel):
    name: str


class ProjectResponse(BaseModel):
    id: int
    name: str


@router.post("/projects/", status_code=status.HTTP_201_CREATED)
async def create_project_api(
    project_create_update_request: ProjectCreateUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserDomain = Depends(get_current_user),
) -> ProjectResponse:
    project = create_project(
        db=db, user_id=current_user.id, name=project_create_update_request.name
    )

    response = ProjectResponse(id=project.id, name=project.name)
    return response


@router.get("/projects/{project_id}")
async def get_project_api(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserDomain = Depends(get_current_user),
) -> ProjectResponse:
    project = get_project(db, project_id=project_id, user_id=current_user.id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    response = ProjectResponse(id=project.id, name=project.name)
    return response


@router.put("/projects/{project_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_project_api(
    project_id: int,
    project_create_update_request: ProjectCreateUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserDomain = Depends(get_current_user),
) -> ProjectResponse:
    project = update_project(
        db,
        project_id=project_id,
        user_id=current_user.id,
        name=project_create_update_request.name,
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    response = ProjectResponse(id=project.id, name=project.name)
    return response


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_api(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserDomain = Depends(get_current_user),
) -> None:
    try:
        delete_project(db, project_id=project_id, user_id=current_user.id)
    except ProjectNotFoundException:
        raise HTTPException(status_code=404, detail="Project not found")


@router.get("/projects/")
async def get_projects_list_api(
    db: Session = Depends(get_db), current_user: UserDomain = Depends(get_current_user)
) -> List[ProjectResponse]:
    projects = list_projects(db=db, user_id=current_user.id)

    response = []
    for project in projects:
        response.append(ProjectResponse(id=project.id, name=project.name))
    return response
