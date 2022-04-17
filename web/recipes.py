from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import HTMLResponse

from core.config import templates
from db.session import database
from repositories.recipe import RecipeRepository
from repositories.recipe_ingredient import RecipeIngredientRepository

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def recipes(request: Request, repository: RecipeRepository = Depends(RecipeRepository)) -> Response:
    return templates.TemplateResponse(
        "recipes.html", {"request": request, "recipes": await repository.list(db=database)}
    )


@router.get("/{title}", response_class=HTMLResponse)
async def recipe(
    title: str,
    request: Request,
    recipe_repository: RecipeRepository = Depends(RecipeRepository),
    recipe_ingredient_repository: RecipeIngredientRepository = Depends(RecipeIngredientRepository),
) -> Response:
    return templates.TemplateResponse(
        "recipe.html",
        {
            "request": request,
            "recipe": await recipe_repository.find(db=database, title=title),
            "ingredients": await recipe_ingredient_repository.list(db=database, recipe_title=title, limit=250),
        },
    )
