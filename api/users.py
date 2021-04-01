from flask import Blueprint, jsonify, abort, request
from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud
import schemas
from db.session import session
from schemas import User

users = Blueprint("users", __name__)


@users.route("/", methods=["GET"])
def index(db: Session = session) -> str:
    return jsonify([User(**user.__dict__).dict() for user in crud.user.list(db=db)])


@users.route("/", methods=["POST"])
def create(db: Session = session) -> tuple:
    try:
        obj_in = schemas.UserCreate(**request.json)
        user = crud.user.create(db=db, obj_in=obj_in)
        return jsonify(User(**user.__dict__).dict()), 201
    except ValidationError as error:
        abort(400, description=str(error))
    except IntegrityError as error:
        if error.orig == UniqueViolation:
            abort(400, description="Resource already exist")


@users.route("/<name>", methods=["GET"])
def read(name: str, db: Session = session) -> str:
    try:
        user = crud.user.get(db=db, name=name)
        return jsonify(User(**user.__dict__).dict())
    except NoResultFound:
        abort(404, description="Resource not found")


@users.route("/<name>", methods=["PATCH"])
def update(name: str, db: Session = session) -> str:
    try:
        user = crud.user.get(db=db, name=name)
        obj_in = schemas.UserUpdate(**request.json)
        crud.user.update(db=db, db_obj=user, obj_in=obj_in)
        return jsonify(User(**user.__dict__).dict())
    except ValidationError as error:
        abort(400, description=str(error))
    except NoResultFound:
        abort(404, description="Resource not found")


@users.route("/<name>", methods=["DELETE"])
def remove(name: str, db: Session = session) -> tuple:
    try:
        crud.user.remove(db=db, model=crud.user.get(db=db, name=name))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")
