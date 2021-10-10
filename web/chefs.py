from typing import Any

from flask import Blueprint, render_template

chefs = Blueprint("chefs", __name__)


@chefs.route("/", methods=["GET"])
def index() -> Any:
    return render_template("chefs.html")
