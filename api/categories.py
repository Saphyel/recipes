from flask import Blueprint, jsonify, abort, request
from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud
import schemas
from db.session import session
from schemas import Category

categories = Blueprint("categories", __name__)


@categories.route("/", methods=["GET"])
def index(db: Session = session):
    return jsonify([Category(**category.__dict__).dict() for category in crud.category.list(db=db)])


@categories.route("/", methods=["POST"])
def create(db: Session = session):
    try:
        obj_in = schemas.CategoryCreate(**request.json)  # type: ignore
        category = crud.category.create(db=db, obj_in=obj_in)
        return jsonify(Category(**category.__dict__).dict()), 201
    except ValidationError as error:
        abort(400, description=str(error))
    except IntegrityError as error:
        if error.orig == UniqueViolation:
            abort(400, description="Resource already exist")
        abort(400, description=str(error))


@categories.route("/<name>", methods=["GET"])
def read(name: str, db: Session = session):
    try:
        category = crud.category.get(db=db, name=name)
        return jsonify(Category(**category.__dict__).dict())
    except NoResultFound:
        abort(404, description="Resource not found")


@categories.route("/<name>", methods=["DELETE"])
def remove(name: str, db: Session = session):
    try:
        crud.category.remove(db=db, model=crud.category.get(db=db, name=name))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")
