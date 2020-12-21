from flask import Flask
from flaskext.mysql import MySQL
from .db import DB
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_DATABASE_USER'] = os.getenv("DB_USER", "pythonfavrepo")
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PASS", "pythonfavrepo")
    app.config['MYSQL_DATABASE_DB'] = os.getenv("DB_NAME", "pythonfavrepo")
    app.config['MYSQL_DATABASE_HOST'] = os.getenv("DB_HOST", "db")
    app.config['MYSQL_DATABASE_CHARSET'] = "utf8mb4"
    app.config['MYSQL_REPO_TABLE_NAME'] = os.getenv("REPO_TABLE_NAME", "repos")
    app.config["RECORDS_PER_PAGE"] = 100
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    else:
        mysql = MySQL(app)
        app.config["DATABASE"] = DB(mysql, app.config['MYSQL_REPO_TABLE_NAME'])
        init_table(mysql, app.config['MYSQL_REPO_TABLE_NAME'])

    from . import repo
    app.register_blueprint(repo.bp)

    from . import repo_list
    app.register_blueprint(repo_list.bp)
    app.add_url_rule('/', endpoint='index')
    return app


def init_table(mysql, table_name):
    conn = mysql.connect()
    try:
        create_table = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                repo_id INTEGER PRIMARY KEY,
                                repo_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                                url VARCHAR(255),
                                created DATETIME,
                                last_push DATETIME,
                                description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                                num_stars INTEGER
                            );"""
        with conn.cursor() as cursor:
            cursor.execute(create_table)
            conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.close()