from datetime import datetime
from .github_api import GitHubAPI
from flask import (
    Blueprint, redirect, render_template, request, url_for, current_app, flash
)

bp = Blueprint('repo_list', __name__)


@bp.route('/')
def index():
    db = current_app.config["DATABASE"]
    records_per_page = current_app.config["RECORDS_PER_PAGE"]
    limit = request.args.get("repo_count", records_per_page)
    repos = db.get_repo_list(limit)
    return render_template('repo/repo_list.html', repo_list=repos, repo_count=limit)


@bp.route('/update', methods=['POST'])
def update():
    repo_count = int(request.form.get("repo_count", 100))
    refresh_data = request.form.get("updateCheckbox", False)
    try:
        if refresh_data:
            upsert_repos(repo_count)
        flash("Updated!")
    except Exception as e:
        flash(f"Unable to Update! {str(e)}")
    return redirect(url_for('repo_list.index', repo_count=repo_count))


def upsert_repos(repo_count: int):
    db = current_app.config["DATABASE"]
    records_per_page = current_app.config["RECORDS_PER_PAGE"]
    api = GitHubAPI()
    base_page_count = int(repo_count / records_per_page)
    pages = base_page_count if repo_count % records_per_page == 0 else base_page_count + 1
    insert_values = []
    for page in range(pages):
        response = api.get_repos_by_stars(page)
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
