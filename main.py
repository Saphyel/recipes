from flask import Flask

from api.categories import categories
from api.recipes import recipes
from db.session import session

app = Flask(__name__)
app.register_blueprint(categories, url_prefix='/api/categories')
app.register_blueprint(recipes, url_prefix='/api/recipes')


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    session.remove()


if __name__ == "__main__":
    app.run()
