from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from core.config import templates
from db.session import get_db

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def recipes(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("recipes.html", {"request": request, "recipes": await crud.recipe.list(db=db)})


@router.get("/{title}", response_class=HTMLResponse)
async def recipe(title: str, request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse(
        "recipe.html",
        {
            "request": request,
            "recipe": await crud.recipe.get(db=db, title=title),
            "ingredients": await crud.recipe_ingredient.list(db=db, recipe_title=title, limit=250),
        },
    )
