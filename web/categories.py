from typing import Any

from flask import Blueprint, render_template
from sqlalchemy.orm import Session

import crud
from db.session import session

categories = Blueprint("categories", __name__)


@categories.route("/", methods=["GET"])
def index(db: Session = session) -> Any:
    return render_template("categories.html", categories=crud.category.list(db=db))


@categories.route("/<name>", methods=["GET"])
def read(name: str, db: Session = session) -> Any:
    return render_template("category.html", category=crud.category.get(db=db, name=name))
