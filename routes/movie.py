from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from models.movie import Movie, MovieCreate
from fastapi.templating import Jinja2Templates
import os
import uuid

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/movie")

movies = [
    Movie(name="Inception", id=1, cost=160000000, director="Christopher Nolan"),
    Movie(name="The Dark Knight", id=2, cost=185000000, director="Christopher Nolan"),
    Movie(name="Pulp Fiction", id=3, cost=8000000, director="Quentin Tarantino"),
    Movie(name="Forrest Gump", id=4, cost=55000000, director="Robert Zemeckis"),
    Movie(name="The Matrix", id=5, cost=63000000, director="Lana Wachowski, Lilly Wachowski"),
    Movie(name="Interstellar", id=6, cost=165000000, director="Christopher Nolan"),
    Movie(name="Fight Club", id=7, cost=63000000, director="David Fincher"),
    Movie(name="The Godfather", id=8, cost=6000000, director="Francis Ford Coppola"),
    Movie(name="Parasite", id=9, cost=11400000, director="Bong Joon-ho"),
    Movie(name="Avengers: Endgame", id=10, cost=356000000, director="Anthony Russo, Joe Russo"),
]

def generate_new_id():
    if movies:
        return max(m.id for m in movies) + 1
    return 1

from routes.auth import verify_jwt_token

def get_current_user_jwt(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail={"message": "Authorization header missing or invalid"})
    token = auth_header[7:]
    return verify_jwt_token(token)

@router.post("/add")
async def add_movie_protected(
    current_user: str = Depends(get_current_user_jwt),
    title: str = Form(...),
    description: str = Form(...),
    release_year: int = Form(...),
    is_available: bool = Form(...),
    description_file: UploadFile = File(None),
    cover_image: UploadFile = File(None)
):
    saved_files = {}
    cover_image_filename = None

    if description_file and description_file.filename:
        original_filename = os.path.basename(description_file.filename)
        if original_filename:
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = f"uploads/{unique_filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await description_file.read())
            saved_files["description_file"] = unique_filename

    if cover_image and cover_image.filename:
        original_filename = os.path.basename(cover_image.filename)
        if original_filename:
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = f"uploads/{unique_filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await cover_image.read())
            saved_files["cover_image"] = unique_filename
            cover_image_filename = unique_filename

    new_movie = Movie(
        name=title,
        id=generate_new_id(),
        cost=0,
        director="",
        cover_image_filename=cover_image_filename
    )

    movies.append(new_movie)

    return {
        "title": title,
        "description": description,
        "release_year": release_year,
        "is_available": is_available,
        "description_file": description_file.filename if description_file else None,
        "cover_image": cover_image.filename if cover_image else None,
        "id": new_movie.id
    }

@router.get("/add", response_class=HTMLResponse)
async def get_add_movie_form(current_user: str = Depends(get_current_user_jwt)):  # Требуется JWT
    return templates.TemplateResponse("add_movie.html", {"request": {}})

@router.get("/add_films", response_class=HTMLResponse)
async def get_add_films_form():
    return templates.TemplateResponse("add_movie.html", {"request": {}})

@router.post("/add_films")
async def add_movie_open(
    title: str = Form(...),
    description: str = Form(...),
    release_year: int = Form(...),
    is_available: bool = Form(...),
    description_file: UploadFile = File(None),
    cover_image: UploadFile = File(None)
):
    saved_files = {}
    cover_image_filename = None

    if description_file and description_file.filename:
        original_filename = os.path.basename(description_file.filename)
        if original_filename:
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = f"uploads/{unique_filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await description_file.read())
            saved_files["description_file"] = unique_filename

    if cover_image and cover_image.filename:
        original_filename = os.path.basename(cover_image.filename)
        if original_filename:
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = f"uploads/{unique_filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await cover_image.read())
            saved_files["cover_image"] = unique_filename
            cover_image_filename = unique_filename

    new_movie = Movie(
        name=title,
        id=generate_new_id(),
        cost=0,
        director="",
        cover_image_filename=cover_image_filename
    )

    movies.append(new_movie)

    return {
        "title": title,
        "description": description,
        "release_year": release_year,
        "is_available": is_available,
        "description_file": description_file.filename if description_file else None,
        "cover_image": cover_image.filename if cover_image else None,
        "id": new_movie.id
    }

@router.get("/top")
async def get_movie_top():
    return movies

@router.get("/{movie_name}")
async def get_movie(movie_name: str) -> Movie | None:
    for movie in movies:
        if movie.name == movie_name:
            return movie

@router.post("/")
async def create_movie(
    title: str = Form(...),
    description: str = Form(...),
    release_year: int = Form(...),
    is_available: bool = Form(...),
    description_file: UploadFile = File(None),
    cover_image: UploadFile = File(None)
):
    saved_files = {}
    cover_image_filename = None

    if description_file and description_file.filename:
        original_filename = os.path.basename(description_file.filename)
        if original_filename:
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = f"uploads/{unique_filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await description_file.read())
            saved_files["description_file"] = unique_filename

    if cover_image and cover_image.filename:
        original_filename = os.path.basename(cover_image.filename)
        if original_filename:
            ext = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4()}{ext}"
            file_path = f"uploads/{unique_filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await cover_image.read())
            saved_files["cover_image"] = unique_filename
            cover_image_filename = unique_filename

    new_movie = Movie(
        name=title,
        id=generate_new_id(),
        cost=0,
        director="",
        cover_image_filename=cover_image_filename
    )

    movies.append(new_movie)

    return {
        "title": title,
        "description": description,
        "release_year": release_year,
        "is_available": is_available,
        "description_file": description_file.filename if description_file else None,
        "cover_image": cover_image.filename if cover_image else None,
        "id": new_movie.id
    }

@router.get("/details/{movie_id}")
async def get_movie_details(movie_id: int):
    movie = next((m for m in movies if m.id == movie_id), None)
    if movie:
        cover_image_url = None
        if movie.cover_image_filename:
            file_path = f"uploads/{movie.cover_image_filename}"
            if os.path.exists(file_path):
                cover_image_url = f"/{file_path}"
        return {
            "id": movie.id,
            "name": movie.name,
            "cost": movie.cost,
            "director": movie.director,
            "cover_image_url": cover_image_url
        }
    return {"error": "Фильм не найден"}