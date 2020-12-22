import pytest
import datetime
from pythonfavrepo import create_app


@pytest.fixture(scope="package")
def app():
    app = create_app({
        'TESTING': True,
        'MYSQL_REPO_TABLE_NAME': "test",
    })

    db = app.config["DATABASE"]
    setup(db.database)
    date = datetime.datetime.strptime("2016-03-20T23:49:42Z", "%Y-%m-%dT%H:%M:%SZ")
    db.store_repos([(1, "Test", "https://test",
                     date,
                     date, "desc", 1,),
                    (2, "Test2", "https://test2",
                     date,
                     date, "desc", 2,)])
    yield app

    teardown(db)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def database(app):
    return app.config["DATABASE"]


def setup(db):
    conn = db.connect()
    try:
        create_table = f"""CREATE TABLE IF NOT EXISTS test(
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


def teardown(db):
    connect = db.database.connect()
    try:
        with connect.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS test")
        connect.commit()
    finally:
        connect.close()
