from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import templates
from db.session import get_db
from repositories.category import category_repository

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def categories(request: Request, db: AsyncSession = Depends(get_db)) -> Response:
    return templates.TemplateResponse(
        "categories.html", {"request": request, "categories": await category_repository.list(db=db)}
    )


@router.get("/{name}", response_class=HTMLResponse)
async def category(name: str, request: Request, db: AsyncSession = Depends(get_db)) -> Response:
    return templates.TemplateResponse(
        "category.html", {"request": request, "category": await category_repository.find(db=db, name=name)}
    )
