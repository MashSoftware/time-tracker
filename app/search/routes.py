from flask import render_template
from flask_login import current_user, login_required

from app import limiter
from app.models import Event
from app.search import bp
from app.search.forms import SearchForm


@bp.route("/", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def search():
    results = []
    form = SearchForm()
    if form.validate_on_submit():
        results = (
            Event.query.filter_by(user_id=current_user.id)
            .filter(Event.comment.ilike("%{}%".format(form.query.data)))
            .order_by(Event.started_at.desc())
            .all()
        )
    return render_template("search.html", title="Search", form=form, results=results)
