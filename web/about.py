from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core.config import templates

router = APIRouter()


@router.get("", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
