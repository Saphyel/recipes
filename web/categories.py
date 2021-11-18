from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from core.config import templates
from db.session import database
from repositories.category import category_repository

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def categories(request: Request) -> Response:
    return templates.TemplateResponse(
        "categories.html", {"request": request, "categories": await category_repository.list(db=database)}
    )


@router.get("/{name}", response_class=HTMLResponse)
async def category(name: str, request: Request) -> Response:
    return templates.TemplateResponse(
        "category.html", {"request": request, "category": await category_repository.find(db=database, name=name)}
    )
