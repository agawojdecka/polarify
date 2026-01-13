from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.project import router as projects_router
from app.api.sentiment_analysis import router as sentiment_analysis_router
from app.api.user import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Polarify App"}


app.include_router(projects_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(sentiment_analysis_router)
