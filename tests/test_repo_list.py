import unittest
from unittest.mock import MagicMock, patch
from pythonfavrepo import create_app
from pythonfavrepo.models import Repo
from pythonfavrepo.github_api import GitHubAPI


class TestRepoList(unittest.TestCase):

    def setUp(self) -> None:
        mock_db = MagicMock()
        mock_db.get_repo_list = MagicMock(return_value=[Repo("1", "TEST_REPO", "https://test",
                                                             "2016-03-20T23:49:42Z",
                                                             "2016-03-20T23:49:42Z", "desc",
                                                             "1"),
                                                        Repo("1", "TEST_REPO_2",
                                                             "https://test2",
                                                             "2016-03-20T23:49:42Z",
                                                             "2016-03-20T23:49:42Z", "desc",
                                                             "2")
                                                        ])
        app = create_app(test_config={"DATABASE": mock_db})
        self.__client = app.test_client()

    def test_index(self):
        response = self.__client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("TEST_REPO" in response.data.decode('utf-8'))
        self.assertTrue("TEST_REPO_2" in response.data.decode('utf-8'))

    @patch.object(GitHubAPI, "get_repos_by_stars")
    def test_update(self, mock_get_repos_by_stars):
        mock_get_repos_by_stars.return_value = {"items": [
            {"id": 1, "full_name": "REPO_NAME", "html_url": "http://test",
             "created_at": "2016-03-20T23:49:42Z", "pushed_at": "2016-03-20T23:49:42Z",
             "description": "desc", "stargazers_count": 1}]}
        response = self.__client.post('/update', data={
            "repo_count": 100,
            "updateCheckbox": True
        })
        self.assertEqual(response.status_code, 302)

    @patch.object(GitHubAPI, "get_repos_by_stars")
    def test_update_exception(self, mock_get_repos_by_stars):
        mock_get_repos_by_stars.return_value = [
            {"pushed_at": "BAD DATA"}]
        response = self.__client.post('/update', data={
            "repo_count": 100,
            "updateCheckbox": True
        })
        self.assertEqual(response.status_code, 302)
