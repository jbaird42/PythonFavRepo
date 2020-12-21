class FailedGitHubRequest(Exception):
    """FailedGitHubRequest is raised when a call to the github api fails"""
    pass


class FailedStoringRepos(Exception):
    """FailedStoringRepos is raised when storage of records to the db fails"""
    pass


class FailedFetchingRecords(Exception):
    """FailedFetchingRecords is raised when retrieval of records from the db fails"""
    pass
