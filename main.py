from fastapi import FastAPI
from routes import study, movie, auth
from fastapi.staticfiles import StaticFiles
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


for route in [study, movie,auth]:
    app.include_router(route.router)
