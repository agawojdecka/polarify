from fastapi import FastAPI

from app.api.analyzer import router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Polarify App"}


app.include_router(router)
