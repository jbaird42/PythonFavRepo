class Repo:
    def __init__(self, repo_id, repo_name, url, created, last_push, description, num_stars):
        self.repo_id = repo_id
        self.repo_name = repo_name
        self.url = url
        self.created = created
        self.last_push = last_push
        self.description = description
        self.num_stars = num_stars
