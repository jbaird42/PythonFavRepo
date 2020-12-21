import unittest
from pythonfavrepo.db import DB
from pythonfavrepo import create_app
from unittest.mock import MagicMock
from pythonfavrepo.exceptions import FailedFetchingRecords, FailedStoringRepos


class TestDB(unittest.TestCase):

    def test_store_repos(self):
        mock_mysql = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.commit = MagicMock()
        mock_mysql.connect = MagicMock(return_value=mock_cursor)
        self.__db = DB(mock_mysql, "test")
        self.__db.store_repos([("1", "Test", "https://test",
                                "2016-03-20T23:49:42Z",
                                "2016-03-20T23:49:42Z", "desc", "1",)])

        mock_cursor.commit.assert_called_once()

    def test_store_repos_exceptions(self):
        mock_mysql = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.commit = MagicMock(side_effect=Exception())
        mock_mysql.connect = MagicMock(return_value=mock_cursor)
        self.__db = DB(mock_mysql, "test")
        with self.assertRaises(FailedStoringRepos):
            self.__db.store_repos([("1", "Test", "https://test",
                                    "2016-03-20T23:49:42Z",
                                    "2016-03-20T23:49:42Z", "desc", "1",)])

    def test_get_repo_list(self):
        mock_mysql = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = (("1", "Test", "https://test",
                                              "2016-03-20T23:49:42Z",
                                              "2016-03-20T23:49:42Z", "desc", "1",),
                                             ("2", "Test2", "https://test2",
                                              "2016-03-20T23:49:42Z",
                                              "2016-03-20T23:49:42Z", "desc", "2",),
                                             )
        mock_mysql.connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        self.__db = DB(mock_mysql, "test")
        results = self.__db.get_repo_list(2)
        self.assertEqual(results[0].repo_name, "Test")
        self.assertEqual(results[1].repo_name, "Test2")

    def test_get_repo(self):
        mock_mysql = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = (("1", "Test", "https://test",
                                              "2016-03-20T23:49:42Z",
                                              "2016-03-20T23:49:42Z", "desc", "1",),
                                             )
        mock_mysql.connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        self.__db = DB(mock_mysql, "test")
        results = self.__db.get_repo(1)
        self.assertEqual(results[0].repo_name, "Test")

    def test_get_repo_exception(self):
        mock_mysql = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = Exception()
        mock_mysql.connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        self.__db = DB(mock_mysql, "test")
        with self.assertRaises(FailedFetchingRecords):
            results = self.__db.get_repo(1)
