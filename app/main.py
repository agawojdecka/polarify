from fastapi import FastAPI

from app.api.analyzer import router as analyzer_router
from app.api.project import router as projects_router
from app.api.user import router as users_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Polarify App"}


app.include_router(analyzer_router)
app.include_router(projects_router)
app.include_router(users_router)
