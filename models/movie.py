from pydantic import BaseModel


class Movie(BaseModel):
    name: str
    id: int
    cost: int
    director: str
    cover_image_filename: str | None = None

class MovieCreate(BaseModel):
    title: str
    description: str
    release_year: int
    is_available: bool