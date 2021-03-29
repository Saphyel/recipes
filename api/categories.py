from flask import Blueprint, jsonify, abort, request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
import schemas
from db.session import session
from schemas import Category

categories = Blueprint("categories", __name__)


@categories.route("/", methods=["GET"])
def index(db: Session = session) -> str:
    categories = [Category(**category.__dict__).dict() for category in crud.category.list(db=db)]
    return jsonify(categories)


@categories.route("/", methods=["POST"])
def create(db: Session = session) -> tuple:
    obj_in = schemas.CategoryCreate(**request.json)
    try:
        category = crud.category.create(db=db, obj_in=obj_in)
        return jsonify(Category(**category.__dict__).dict()), 201
    except IntegrityError as error:
        abort(400, description=error)


@categories.route("/<name>", methods=["GET"])
def read(name: str, db: Session = session) -> str:
    category = crud.category.get(db=db, name=name)
    if not category:
        abort(404, description="Resource not found")
    return jsonify(Category(**category.__dict__).dict())


@categories.route("/<name>", methods=["DELETE"])
def remove(name: str, db: Session = session) -> tuple:
    category = crud.category.get(db=db, name=name)
    if not category:
        abort(404, description="Resource not found")
    crud.category.remove(db=db, model=category)
    return jsonify(), 204
