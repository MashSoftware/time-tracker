from app import limiter
from app.search import bp
from flask import render_template
from flask_login import current_user, login_required
from app.search.forms import SearchForm
from app.models import Event


@bp.route("/", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = Event.query.filter(Event.comment.ilike("%{}%".format(form.query.data))).all()
        return render_template("search/search.html", title="Search", form=form, results=results)
    return render_template("search/search.html", title="Search", form=form)
