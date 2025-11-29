from fastapi import FastAPI
from routes import study, movie, auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


for route in [study, movie,auth]:
    app.include_router(route.router)
