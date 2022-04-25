from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import HTMLResponse

from core.config import templates
from repositories.recipe import RecipeRepository
from repositories.recipe_ingredient import RecipeIngredientRepository

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def recipes(request: Request, repository: RecipeRepository = Depends(RecipeRepository)) -> Response:
    return templates.TemplateResponse("recipes.html", {"request": request, "recipes": await repository.list()})


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
            "recipe": await recipe_repository.find(title=title),
            "ingredients": await recipe_ingredient_repository.list(recipe_title=title, limit=250),
        },
    )
