from flask import Flask

from db.session import session

app = Flask(__name__)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    session.remove()


if __name__ == "__main__":
    app.run()
