from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

import api
import web
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(GZipMiddleware)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(api.chefs.router, prefix="/api/chefs", tags=["chefs"])
app.include_router(api.recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(api.ingredients.router, prefix="/api/ingredients", tags=["ingredients"])
app.include_router(api.users.router, prefix="/api/users", tags=["users"])
app.include_router(api.tokens.router, prefix="/api", tags=["login"])

app.include_router(web.about.router, prefix="/about", tags=["public ui"])
app.include_router(web.categories.router, prefix="/categories", tags=["public ui"])
app.include_router(web.chefs.router, prefix="/chefs", tags=["public ui"])
app.include_router(web.recipes.router, prefix="/recipes", tags=["public ui"])
