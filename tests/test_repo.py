import unittest
from unittest.mock import MagicMock
from pythonfavrepo import create_app
from pythonfavrepo.models import Repo


class TestRepo(unittest.TestCase):

    def test_get_repo(self):
        mock_get_repo = MagicMock()
        mock_get_repo.get_repo = MagicMock(return_value=[Repo("1", "TEST_REPO", "https://test",
                                                             "2016-03-20T23:49:42Z",
                                                             "2016-03-20T23:49:42Z", "desc", "1")])
        app = create_app(test_config={"DATABASE": mock_get_repo})
        client = app.test_client()
        response = client.get('/repo/1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("TEST_REPO" in response.data.decode('utf-8'))

    def test_get_repo_failure(self):
        mock_get_repo = MagicMock()
        mock_get_repo.get_repo = MagicMock(return_value=None)
        app = create_app(test_config={"DATABASE": mock_get_repo})
        client = app.test_client()
        response = client.get('/repo/1')
        self.assertEqual(response.status_code, 302)
