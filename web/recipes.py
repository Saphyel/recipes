from typing import Any

from flask import Blueprint, render_template
from sqlalchemy.orm import Session

import crud
from db.session import session

recipes = Blueprint("recipes", __name__)


@recipes.route("/", methods=["GET"])
def index(db: Session = session) -> Any:
    return render_template("recipes.html", recipes=crud.recipe.list(db=db))


@recipes.route("/<title>", methods=["GET"])
def read(title: str, db: Session = session) -> Any:
    return render_template("recipe.html", recipe=crud.recipe.get(db=db, title=title))
