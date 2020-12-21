import unittest
import requests_mock
from pythonfavrepo.github_api import GitHubAPI
from pythonfavrepo.exceptions import FailedGitHubRequest


class TestGitHubApi(unittest.TestCase):

    def setUp(self) -> None:
        self.__githubapi = GitHubAPI()

    @requests_mock.Mocker()
    def test_get_repos_by_stars(self, m):
        m.get("https://api.github.com/search/repositories", json={"repo": "success"})
        result = self.__githubapi.get_repos_by_stars(page=1)
        self.assertEqual(result.get("repo"), "success")

    @requests_mock.Mocker()
    def test_get_repos_by_stars_exception(self, m):
        m.get("https://api.github.com/search/repositories", status_code=500)
        with self.assertRaises(FailedGitHubRequest):
            result = self.__githubapi.get_repos_by_stars(page=1)
