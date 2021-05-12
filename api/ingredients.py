from flask import Blueprint, jsonify, abort, request
from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud
import schemas
from db.session import session
from schemas import Ingredient

ingredients = Blueprint("ingredients", __name__)


@ingredients.route("/", methods=["GET"])
def index(db: Session = session):
    return jsonify([Ingredient(**ingredient.__dict__).dict() for ingredient in crud.ingredient.list(db=db)])


@ingredients.route("/", methods=["POST"])
def create(db: Session = session):
    try:
        obj_in = schemas.IngredientCreate(**request.json)  # type: ignore
        ingredient = crud.ingredient.create(db=db, obj_in=obj_in)
        return jsonify(Ingredient(**ingredient.__dict__).dict()), 201
    except ValidationError as error:
        abort(400, description=str(error))
    except IntegrityError as error:
        if error.orig == UniqueViolation:
            abort(400, description="Resource already exist")
        abort(400, description=str(error))


@ingredients.route("/<name>", methods=["GET"])
def read(name: str, db: Session = session):
    try:
        ingredient = crud.ingredient.get(db=db, name=name)
        return jsonify(Ingredient(**ingredient.__dict__).dict())
    except NoResultFound:
        abort(404, description="Resource not found")


@ingredients.route("/<name>", methods=["DELETE"])
def remove(name: str, db: Session = session):
    try:
        crud.ingredient.remove(db=db, model=crud.ingredient.get(db=db, name=name))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")
