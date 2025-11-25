from fastapi import APIRouter, Depends, HTTPException, status

from app.crud.project import create_project, get_project
from app.database import Base, engine, get_db
from app.models.project import Project

router = APIRouter()
Base.metadata.create_all(bind=engine)


@router.post("/projects/", status_code=status.HTTP_201_CREATED)
async def create_project_api(name: str, db=Depends(get_db)):
    return create_project(db=db, name=name)


@router.get("/projects/{project_id}")
async def get_project_api(project_id: int, db=Depends(get_db)):
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_project_api(project_id: int, name: str, db=Depends(get_db)):
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = name
    db.commit()
    db.refresh(project)

    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_project_api(project_id: int, db=Depends(get_db)):
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()

    return {"detail": "Project deleted"}


@router.get("/projects/")
async def get_projects_list_api(db=Depends(get_db)):
    projects = db.query(Project).all()
    return projects
