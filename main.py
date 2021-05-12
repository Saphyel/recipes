import gzip

from flask import Flask, json, request
from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response

import api
from db.session import session

app = Flask(__name__)
app.register_blueprint(api.categories, url_prefix="/api/categories")
app.register_blueprint(api.users, url_prefix="/api/users")
app.register_blueprint(api.recipes, url_prefix="/api/recipes")
app.register_blueprint(api.ingredients, url_prefix="/api/ingredients")


@app.teardown_appcontext
def remove_session(*args, **kwargs) -> None:
    session.remove()


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> Response:
    response = error.get_response()
    response.content_type = "application/json"
    response.data = json.dumps({"error": error.description})  # type: ignore
    return response


@app.after_request
def add_compression(response: Response) -> Response:
    if request.path.startswith("/static/"):
        return response
    response.data = gzip.compress(response.data, 5)  # type: ignore
    response.headers["Content-Encoding"] = "gzip"
    response.headers["Content-length"] = len(response.data)  # type: ignore
    return response


if __name__ == "__main__":
    app.run()
