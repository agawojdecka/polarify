from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectNotFoundException(Exception):
    pass


def create_project(
    db: Session, user_id: int, name: str, description: str | None
) -> Project:
    db_project = Project(
        user_id=user_id, name=name, description=description if description else ""
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def get_project(db: Session, project_id: int, user_id: int) -> Project | None:
    db_project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == user_id)
        .first()
    )
    if not db_project:
        return None

    return db_project


def update_project(
    db: Session, project_id: int, user_id: int, name: str, description: str | None
) -> Project | None:
    db_project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == user_id)
        .first()
    )
    if not db_project:
        return None

    db_project.name = name
    db_project.description = description if description else None  # type: ignore
    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: int, user_id: int) -> None:
    db_project = get_project(db, project_id=project_id, user_id=user_id)
    if db_project is None:
        raise ProjectNotFoundException
    db.delete(db_project)
    db.commit()


def list_projects(db: Session, user_id: int) -> list[Project]:
    db_projects_list = db.query(Project).filter(Project.user_id == user_id).all()
    return db_projects_list
