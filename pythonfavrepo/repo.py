from flask import (
    Blueprint, render_template, current_app, redirect, url_for
)

bp = Blueprint('repo', __name__, url_prefix='/repo')

@bp.route('/<int:repo_id>', methods=['GET'])
def get_repo(repo_id: int):
    db = current_app.config["DATABASE"]
    repo = db.get_repo(repo_id)
    if repo:
        return render_template('repo/repo.html', repo=repo[0])
    return redirect(url_for('repo_list.index'))
