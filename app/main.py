from fastapi import FastAPI

from app.api.analyzer import router as analyzer_router
from app.api.projects import router as projects_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Polarify App"}


app.include_router(analyzer_router)
app.include_router(projects_router)
