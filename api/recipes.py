from flask import Blueprint, jsonify, abort, request
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

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
    try:
        obj_in = schemas.RecipeCreate(**request.json)
        recipe = crud.recipe.create(db=db, obj_in=obj_in)
        return jsonify(Recipe(**recipe.__dict__).dict()), 201
    except ValidationError as error:
        abort(400, description=str(error))
    except IntegrityError as error:
        if error.orig == UniqueViolation:
            abort(400, description="Resource already exist")
        if error.orig == ForeignKeyViolation:
            abort(400, description="Foreign resources not found")


@recipes.route("/<title>", methods=["GET"])
def read(title: str, db: Session = session) -> str:
    try:
        recipe = crud.recipe.get(db=db, title=title)
        return jsonify(Recipe(**recipe.__dict__).dict())
    except NoResultFound:
        abort(404, description="Resource not found")


@recipes.route("/<name>", methods=["PATCH"])
def update(name: str, db: Session = session) -> str:
    try:
        recipe = crud.recipe.get(db=db, name=name)
        obj_in = schemas.RecipeUpdate(**request.json)
        crud.recipe.update(db=db, db_obj=recipe, obj_in=obj_in)
        return jsonify(Recipe(**recipe.__dict__).dict())
    except ValidationError as error:
        abort(400, description=str(error))
    except NoResultFound:
        abort(404, description="Resource not found")
    except IntegrityError as error:
        if error.orig == ForeignKeyViolation:
            abort(400, description="Foreign resources not found")


@recipes.route("/<title>", methods=["DELETE"])
def remove(title: str, db: Session = session) -> tuple:
    try:
        crud.recipe.remove(db=db, model=crud.recipe.get(db=db, title=title))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")
