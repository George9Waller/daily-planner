import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_babel import Babel

import routes
from actions.printing import create_instant_print_job
from data import db, migrate
from printing.execute import print_label

load_dotenv()

# app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db.init_app(app)
migrate.init_app(app, db)

app.add_url_rule("/", view_func=routes.home)
app.add_url_rule("/print", view_func=routes.print_now, methods=["POST"])


# internationalization
def get_locale():
    # TODO: add en_GB back
    return request.accept_languages.best_match(["fr_FR"])


babel = Babel(
    app,
    locale_selector=get_locale,
    default_locale=os.environ.get("BABEL_DEFAULT_LOCALE"),
)


@app.cli.command("print-now")
def print_now():
    print_data = create_instant_print_job(locale="fr_FR")
    print_label(print_data)
