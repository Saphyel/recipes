from flask import Blueprint, jsonify, abort, request
from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud
import schemas
from db.session import session
from schemas import Chef

chefs = Blueprint("api chefs", __name__)


@chefs.route("/", methods=["GET"])
def index(db: Session = session):
    return jsonify([Chef(**chef.__dict__).dict() for chef in crud.chef.list(db=db)])


@chefs.route("/", methods=["POST"])
def create(db: Session = session):
    try:
        obj_in = schemas.ChefCreate(**request.json)  # type: ignore
        chef = crud.chef.create(db=db, obj_in=obj_in)
        return jsonify(Chef(**chef.__dict__).dict()), 201
    except ValidationError as error:
        abort(400, description=str(error))
    except IntegrityError as error:
        if error.orig == UniqueViolation:
            abort(400, description="Resource already exist")
        abort(400, description=str(error))


@chefs.route("/<name>", methods=["GET"])
def read(name: str, db: Session = session):
    try:
        chef = crud.chef.get(db=db, name=name)
        return jsonify(Chef(**chef.__dict__).dict())
    except NoResultFound:
        abort(404, description="Resource not found")


@chefs.route("/<name>", methods=["PATCH"])
def update(name: str, db: Session = session):
    try:
        chef = crud.chef.get(db=db, name=name)
        obj_in = schemas.ChefUpdate(**request.json)  # type: ignore
        crud.chef.update(db=db, db_obj=chef, obj_in=obj_in)
        return jsonify(Chef(**chef.__dict__).dict())
    except ValidationError as error:
        abort(400, description=str(error))
    except NoResultFound:
        abort(404, description="Resource not found")


@chefs.route("/<name>", methods=["DELETE"])
def remove(name: str, db: Session = session):
    try:
        crud.chef.remove(db=db, model=crud.chef.get(db=db, name=name))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")
