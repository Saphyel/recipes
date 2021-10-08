from flask import Blueprint, jsonify, abort, request
from psycopg2.errors import UniqueViolation
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

import crud
import schemas
from db.session import session
from schemas import Profile

profiles = Blueprint("api profiles", __name__)


@profiles.route("/", methods=["GET"])
def index(db: Session = session):
    return jsonify([Profile(**profile.__dict__).dict() for profile in crud.profile.list(db=db)])


@profiles.route("/", methods=["POST"])
def create(db: Session = session):
    try:
        obj_in = schemas.ProfileCreate(**request.json)  # type: ignore
        profile = crud.profile.create(db=db, obj_in=obj_in)
        return jsonify(Profile(**profile.__dict__).dict()), 201
    except ValidationError as error:
        abort(400, description=str(error))
    except IntegrityError as error:
        if error.orig == UniqueViolation:
            abort(400, description="Resource already exist")
        abort(400, description=str(error))


@profiles.route("/<name>", methods=["GET"])
def read(name: str, db: Session = session):
    try:
        profile = crud.profile.get(db=db, name=name)
        return jsonify(Profile(**profile.__dict__).dict())
    except NoResultFound:
        abort(404, description="Resource not found")


@profiles.route("/<name>", methods=["PATCH"])
def update(name: str, db: Session = session):
    try:
        profile = crud.profile.get(db=db, name=name)
        obj_in = schemas.ProfileUpdate(**request.json)  # type: ignore
        crud.profile.update(db=db, db_obj=profile, obj_in=obj_in)
        return jsonify(Profile(**profile.__dict__).dict())
    except ValidationError as error:
        abort(400, description=str(error))
    except NoResultFound:
        abort(404, description="Resource not found")


@profiles.route("/<name>", methods=["DELETE"])
def remove(name: str, db: Session = session):
    try:
        crud.profile.remove(db=db, model=crud.profile.get(db=db, name=name))
        return jsonify(), 204
    except NoResultFound:
        abort(404, description="Resource not found")
