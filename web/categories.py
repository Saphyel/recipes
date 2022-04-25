from core.config import templates
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import HTMLResponse
from repositories.category import CategoryRepository

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def categories(request: Request, repository: CategoryRepository = Depends(CategoryRepository)) -> Response:
    return templates.TemplateResponse("categories.html", {"request": request, "categories": await repository.list()})


@router.get("/{name}", response_class=HTMLResponse)
async def category(
    name: str, request: Request, repository: CategoryRepository = Depends(CategoryRepository)
) -> Response:
    return templates.TemplateResponse(
        "category.html", {"request": request, "category": await repository.find(name=name)}
    )
