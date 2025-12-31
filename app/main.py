from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.analyzer import router as analyzer_router
from app.api.auth import router as auth_router
from app.api.dependencies.database import Base, engine
from app.api.project import router as projects_router
from app.api.sentiment_analysis import router as sentiment_analysis_router
from app.api.user import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to Polarify App"}


app.include_router(analyzer_router)
app.include_router(projects_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(sentiment_analysis_router)
