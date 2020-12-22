from flask import Flask
from flaskext.mysql import MySQL
from .db import DB
from .repo_list import upsert_repos
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USER", "pythonfavrepo")
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PASS", "pythonfavrepo")
    app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME", "pythonfavrepo")
    app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST", "localhost")
    app.config['MYSQL_DATABASE_CHARSET'] = "utf8mb4"
    app.config['MYSQL_REPO_TABLE_NAME'] = os.getenv("REPO_TABLE_NAME", "repos")
    app.config["RECORDS_PER_PAGE"] = 100
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    mysql = MySQL(app)
    app.config["DATABASE"] = DB(mysql, app.config['MYSQL_REPO_TABLE_NAME'])

    from . import repo
    app.register_blueprint(repo.bp)

    from . import repo_list
    app.register_blueprint(repo_list.bp)
    app.add_url_rule('/', endpoint='index')

    if not app.config["TESTING"]:
        # Preload data if not testing
        with app.app_context():
            upsert_repos(app.config["RECORDS_PER_PAGE"])

    return app
