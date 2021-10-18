from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from core.config import templates

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def about(request: Request) -> Response:
    return templates.TemplateResponse("about.html", {"request": request})
