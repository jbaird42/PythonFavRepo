import datetime
from pythonfavrepo.exceptions import FailedFetchingRecords, FailedStoringRepos
import pytest


def test_store_repos(database):
    date = datetime.datetime.strptime("2016-03-20T23:49:42Z", "%Y-%m-%dT%H:%M:%SZ")
    items_stored = database.store_repos([(1234, "StoreTest", "https://test",
                                          date,
                                          date, "desc", "1",)])
    assert items_stored == 1


def test_store_repos_exception(database):
    with pytest.raises(FailedStoringRepos):
        database.store_repos([1])


def test_get_repo_list(database):
    results = database.get_repo_list(2)
    assert len(results) == 2
    assert results[0].repo_name is not None


def test_get_repo(database):
    results = database.get_repo(1)
    assert len(results) == 1
    assert results[0].repo_name == "Test"
