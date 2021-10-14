from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

import api
import web
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(GZipMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(api.chefs.router, prefix="/api/chefs", tags=["chefs"])
app.include_router(api.recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(api.ingredients.router, prefix="/api/ingredients", tags=["ingredients"])
app.include_router(web.about.router, prefix="/about", tags=["html"])
app.include_router(web.categories.router, prefix="/categories", tags=["html"])
app.include_router(web.chefs.router, prefix="/chefs", tags=["html"])
app.include_router(web.recipes.router, prefix="/recipes", tags=["html"])
