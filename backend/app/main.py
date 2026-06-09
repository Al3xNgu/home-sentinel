from fastapi import FastAPI
from app import database
from app.routes.people import router as people_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Smart Home Facial Recognition API is running"}

app.include_router(people_router)