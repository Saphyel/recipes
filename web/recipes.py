from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import templates
from db.session import get_db
from repositories.recipe_ingredient import recipe_ingredient_repository
from repositories.recipe import recipe_repository

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def recipes(request: Request, db: AsyncSession = Depends(get_db)) -> Response:
    return templates.TemplateResponse(
        "recipes.html", {"request": request, "recipes": await recipe_repository.list(db=db)}
    )


@router.get("/{title}", response_class=HTMLResponse)
async def recipe(title: str, request: Request, db: AsyncSession = Depends(get_db)) -> Response:
    return templates.TemplateResponse(
        "recipe.html",
        {
            "request": request,
            "recipe": await recipe_repository.find(db=db, title=title),
            "ingredients": await recipe_ingredient_repository.list(db=db, recipe_title=title, limit=250),
        },
    )
