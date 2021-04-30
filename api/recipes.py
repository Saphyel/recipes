from flask import Blueprint, jsonify, abort, request
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud
import schemas
from db.session import session
from schemas import Recipe, RecipeIngredient

recipes = Blueprint("recipes", __name__)


@recipes.route("/", methods=["GET"])
def index(db: Session = session):
    return jsonify([Recipe(**recipe.__dict__).dict() for recipe in crud.recipe.list(db=db)])


@recipes.route("/", methods=["POST"])
def create(db: Session = session):
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
        abort(400, description=str(error))


@recipes.route("/<title>", methods=["GET"])
def read(title: str, db: Session = session):
    try:
        recipe = crud.recipe.get(db=db, title=title)
        return jsonify(Recipe(**recipe.__dict__).dict())
    except NoResultFound:
        abort(404, description="Resource not found")


@recipes.route("/<title>", methods=["PATCH"])
def update(title: str, db: Session = session):
    try:
        recipe = crud.recipe.get(db=db, title=title)
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
        abort(400, description=str(error))


@recipes.route("/<title>", methods=["DELETE"])
def remove(title: str, db: Session = session):
    try:
        crud.recipe.remove(db=db, model=crud.recipe.get(db=db, title=title))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")


@recipes.route("/<title>/ingredients", methods=["GET"])
def index(title: str, db: Session = session):
    return jsonify(
        [RecipeIngredient(**ingredient.__dict__).dict() for ingredient in
         crud.recipe_ingredient.list(db=db, recipe_title=title)]
    )


@recipes.route("/<title>/ingredients/<name>", methods=["DELETE"])
def index(title: str, name:str, db: Session = session):
    try:
        crud.recipe_ingredient.remove(db=db, model=crud.recipe_ingredient.get(db=db, title=title, name=name))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")
