from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from core.config import templates
from db.session import get_db

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def categories(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse(
        "categories.html", {"request": request, "categories": await crud.category.list(db=db)}
    )


@router.get("/{name}", response_class=HTMLResponse)
async def category(name: str, request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse(
        "category.html", {"request": request, "category": await crud.category.get(db=db, name=name)}
    )
