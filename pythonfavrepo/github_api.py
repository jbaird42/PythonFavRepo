import requests
from .exceptions import FailedGitHubRequest


class GitHubAPI:

    def get_repos_by_stars(self, page: int) -> dict:
        payload = {"q": "language:python", "sort": "stars", "order": "desc", "page": f"{page}",
                   "per_page": "100"}
        return self.__call_search_repositories(payload)

    @staticmethod
    def __call_search_repositories(payload: dict) -> dict:
        """
        Calls the github search repositories endpoint with the provided payload (query string)
        :param payload: dict containing values to be sent in the query string
        :return: results dict
        """
        try:
            response = requests.get(url="https://api.github.com/search/repositories",
                                    params=payload)
            if response.status_code != 200:
                raise Exception()
            return response.json()
        except Exception:
            raise FailedGitHubRequest("Failed GitHub Request")