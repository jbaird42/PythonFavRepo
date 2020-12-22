from datetime import datetime
from .github_api import GitHubAPI
from flask import (
    Blueprint, redirect, render_template, request, url_for, current_app, flash
)

bp = Blueprint('repo_list', __name__)


@bp.route('/')
def index():
    db = current_app.config["DATABASE"]
    limit = validate_repo_count(request.args.get("repo_count"))
    repos = db.get_repo_list(limit)
    return render_template('repo/repo_list.html', repo_list=repos, repo_count=limit, showing=len(repos))


@bp.route('/update', methods=['POST'])
def update():
    repo_count = validate_repo_count(request.form.get("repo_count"))
    use_local = request.form.get("useLocalCheckbox", False)
    try:
        if not use_local:
            upsert_repos(repo_count)
            flash("Updated!")
        else:
            flash("Updated using local data! If the table shows less results than you requested"\
                  " then disable 'Use local data only' and try again.")
    except Exception as e:
        flash(f"Unable to Update! {str(e)}")
    return redirect(url_for('repo_list.index', repo_count=repo_count))


def upsert_repos(repo_count: int):
    """
    upsert_repos updates/inserts repositories list by calling github api and saving the results in mysql.
    :param repo_count: number of repos to upsert
    :return:
    """
    db = current_app.config["DATABASE"]
    records_per_page = current_app.config["RECORDS_PER_PAGE"]
    api = GitHubAPI()
    base_page_count = int(repo_count / records_per_page)
    pages = base_page_count if repo_count % records_per_page == 0 else base_page_count + 1
    insert_values = []
    for page in range(pages):
        response = api.get_repos_by_stars(page+1)
        for repo in response['items']:
            insert_values.append((
                repo.get("id"),
                repo.get("full_name", ""),
                repo.get("html_url"),
                datetime.strptime(repo.get("created_at"), "%Y-%m-%dT%H:%M:%SZ"),
                datetime.strptime(repo.get("pushed_at"), "%Y-%m-%dT%H:%M:%SZ"),
                repo.get("description", ""),
                repo.get("stargazers_count"),
            ))
    db.store_repos(insert_values)


def validate_repo_count(repo_count):
    """
    Validate that repo_count is an int. if not then set default
    :param repo_count: integer
    :return:
    """
    try:
        return int(repo_count)
    except Exception:
        return current_app.config["RECORDS_PER_PAGE"]
