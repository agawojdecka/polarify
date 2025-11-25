from sqlalchemy.orm import Session

from app.models.project import Project


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, name: str):
    project = Project(name=name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
