import gzip
from typing import Any

from flask import Flask, json, request
from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response

import api
import web
from db.session import session

app = Flask(__name__)
app.register_blueprint(api.categories, url_prefix="/api/categories")
app.register_blueprint(api.profiles, url_prefix="/api/profiles")
app.register_blueprint(api.recipes, url_prefix="/api/recipes")
app.register_blueprint(api.ingredients, url_prefix="/api/ingredients")
app.register_blueprint(web.about, url_prefix="/about")
app.register_blueprint(web.categories, url_prefix="/categories")
app.register_blueprint(web.profiles, url_prefix="/profiles")
app.register_blueprint(web.recipes, url_prefix="/recipes")


@app.teardown_appcontext
def remove_session(*args, **kwargs) -> Any:
    session.remove()


@app.errorhandler(HTTPException)  # type: ignore
def handle_exception(error: HTTPException) -> Any:
    response = error.get_response()
    response.content_type = "application/json"
    response.data = json.dumps({"error": error.description})  # type: ignore
    return response


@app.after_request
def add_compression(response: Response) -> Any:
    if request.path.startswith("/static/"):
        return response
    response.data = gzip.compress(response.data, 5)  # type: ignore
    response.headers["Content-Encoding"] = "gzip"
    response.headers["Content-length"] = len(response.data)  # type: ignore
    return response


if __name__ == "__main__":
    app.run()
