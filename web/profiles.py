from typing import Any

from flask import Blueprint, render_template

profiles = Blueprint("profiles", __name__)


@profiles.route("/", methods=["GET"])
def index() -> Any:
    return render_template("profiles.html")
