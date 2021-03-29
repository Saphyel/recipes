from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from db.session import session
from schemas import Recipe

recipes = Blueprint("recipes", __name__)


@recipes.route("/", methods=["GET"])
def index(db: Session = session) -> str:
    return jsonify([Recipe(**recipe.__dict__).dict() for recipe in crud.recipe.list(db=db)])


@recipes.route("/", methods=["POST"])
def create(db: Session = session) -> tuple:
    obj_in = schemas.RecipeCreate(**request.json)
    try:
        recipe = crud.recipe.create(db=db, obj_in=obj_in)
        return jsonify(Recipe(**recipe.__dict__).dict()), 201
    except IntegrityError as error:
        abort(400, description=error)


@recipes.route("/<title>", methods=["GET"])
def read(title: str, db: Session = session) -> str:
    recipe = crud.recipe.get(db=db, title=title)
    if not recipe:
        abort(404, description="Resource not found")
    return jsonify(Recipe(**recipe.__dict__).dict())


@recipes.route("/<title>", methods=["DELETE"])
def remove(title: str, db: Session = session) -> tuple:
    recipe = crud.recipe.get(db=db, title=title)
    if not recipe:
        abort(404, description="Resource not found")
    crud.recipe.remove(db=db, model=recipe)
    return jsonify(), 204
