from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from core.config import templates
from db.session import database
from repositories.recipe import recipe_repository
from repositories.recipe_ingredient import recipe_ingredient_repository

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def recipes(request: Request) -> Response:
    return templates.TemplateResponse(
        "recipes.html", {"request": request, "recipes": await recipe_repository.list(db=database)}
    )


@router.get("/{title}", response_class=HTMLResponse)
async def recipe(title: str, request: Request) -> Response:
    return templates.TemplateResponse(
        "recipe.html",
        {
            "request": request,
            "recipe": await recipe_repository.find(db=database, title=title),
            "ingredients": await recipe_ingredient_repository.list(db=database, recipe_title=title, limit=250),
        },
    )
