from flask import Flask, json
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response
from api.categories import categories
from api.recipes import recipes
from api.users import users
from db.session import session

app = Flask(__name__)
app.register_blueprint(categories, url_prefix='/api/categories')
app.register_blueprint(recipes, url_prefix='/api/recipes')
app.register_blueprint(users, url_prefix='/api/users')


@app.teardown_appcontext
def remove_session(*args, **kwargs) -> None:
    session.remove()


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> Response:
    response = error.get_response()
    response.content_type = "application/json"
    response.data = json.dumps({"error": error.description})
    return response


if __name__ == "__main__":
    app.run()