from .models import Repo
from .exceptions import FailedStoringRepos, FailedFetchingRecords


class DB:

    def __init__(self, db, repo_table_name):
        self.__db = db
        self.__table_name = repo_table_name

    def store_repos(self, insert_values: list):
        connect = self.__db.connect()
        num_added = 0
        try:
            with connect.cursor() as cursor:
                add_repos = f"""INSERT INTO {self.__table_name} (repo_id, repo_name, url, created, last_push, description, num_stars)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE
                                    repo_name = VALUES(repo_name),
                                    url = VALUES(url),
                                    created = VALUES(created),
                                    last_push = VALUES(last_push),
                                    description = VALUES(description),
                                    num_stars = VALUES(num_stars)"""
                num_added = cursor.executemany(add_repos, insert_values)
            connect.commit()
        except Exception as e:
            raise FailedStoringRepos(f"Failed to store records. {str(e)}")
        finally:
            connect.close()
        return num_added

    def get_repo_list(self, repo_count: int):
        get_repos = f"SELECT * FROM {self.__table_name} ORDER BY num_stars DESC LIMIT {repo_count}"
        results = self.__fetch_records(get_repos)
        return self.__build_model(results)

    def get_repo(self, repo_id):
        get_repos = f"SELECT * FROM {self.__table_name} WHERE repo_id = {repo_id}"
        result = self.__fetch_records(get_repos)
        return self.__build_model(result)

    def __fetch_records(self, query):
        connect = self.__db.connect()
        try:
            with connect.cursor() as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
            return records
        except Exception as e:
            raise FailedFetchingRecords(f"Failed to retrieve records. {str(e)}")
        finally:
            connect.close()

    @staticmethod
    def __build_model(result) -> list:
        repo_list = []
        for item in result:
            repo_list.append(Repo(
                repo_id=item[0],
                repo_name=item[1],
                url=item[2],
                created=item[3],
                last_push=item[4],
                description=item[5],
                num_stars=item[6]
            ))
        return repo_list
