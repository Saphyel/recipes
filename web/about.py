from typing import Any

from flask import Blueprint, render_template

about = Blueprint("about", __name__)


@about.route("/", methods=["GET"])
def index() -> Any:
    return render_template("about.html")
