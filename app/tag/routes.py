from datetime import datetime

import pytz
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, fresh_login_required, login_required
from werkzeug.exceptions import Forbidden

from app import csrf, db, limiter
from app.models import Tag
from app.tag import bp
from app.tag.forms import DefaultForm, TagForm
from app.utils import seconds_to_decimal, seconds_to_string


@bp.route("/")
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def tags():
    now = pytz.utc.localize(datetime.utcnow())
    for tag in current_user.tags:
        total_seconds = 0
        for event in tag.events:
            total_seconds += event.duration(end=now)

        tag.total_string = seconds_to_string(total_seconds)
        tag.total_decimal = seconds_to_decimal(total_seconds)

    return render_template("tag/tags.html", title="Tags")


@bp.route("/new", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def create():
    if len(current_user.tags) == current_user.tag_limit:
        flash(
            "You have reached the {0} tag limit for your account. "
            "Please delete an existing tag in order to create a new one.".format(current_user.tag_limit),
            "info",
        )
        return redirect(url_for("tag.tags"))
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(user_id=current_user.id, name=form.name.data.strip())
        db.session.add(tag)
        db.session.commit()
        current_app.logger.info("User {} created tag {}".format(current_user.id, tag.id))
        flash("Tag has been created.", "success")
        return redirect(url_for("tag.tags"))
    return render_template("tag/create_tag_form.html", title="Create tag", form=form)


@bp.route("/<uuid:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def update(id):
    tag = Tag.query.get_or_404(str(id), description="Tag not found")
    if tag not in current_user.tags:
        raise Forbidden()
    form = TagForm()
    if form.validate_on_submit():
        tag.name = form.name.data.strip()
        tag.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(tag)
        db.session.commit()
        current_app.logger.info("User {} updated tag {}".format(current_user.id, tag.id))
        flash("Tag has been saved.", "success")
        return redirect(url_for("tag.tags"))
    elif request.method == "GET":
        form.name.data = tag.name
    return render_template("tag/update_tag_form.html", title="Edit tag", form=form, tag=tag)


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
@csrf.exempt
@fresh_login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def delete(id):
    tag = Tag.query.get_or_404(str(id), description="Tag not found")
    if tag not in current_user.tags:
        raise Forbidden()
    if request.method == "GET":
        now = pytz.utc.localize(datetime.utcnow())
        total_seconds = 0
        for event in tag.events:
            total_seconds += event.duration(end=now)

        tag.total_string = seconds_to_string(total_seconds)
        tag.total_decimal = seconds_to_decimal(total_seconds)

        return render_template("tag/delete_tag.html", title="Delete tag", tag=tag)
    elif request.method == "POST":
        current_app.logger.info("User {} deleted tag {}".format(current_user.id, tag.id))
        db.session.delete(tag)
        db.session.commit()
        flash("Tag has been deleted.", "success")
        return redirect(url_for("tag.tags"))


@bp.route("/<uuid:id>/entries", methods=["GET"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def entries(id):
    tag = Tag.query.get_or_404(str(id), description="Tag not found")
    if tag not in current_user.tags:
        raise Forbidden()
    now = pytz.utc.localize(datetime.utcnow())

    total_seconds = 0
    for event in tag.events:
        total_seconds += event.duration(end=now)

    total_string = seconds_to_string(total_seconds)
    total_decimal = seconds_to_decimal(total_seconds)

    return render_template(
        "tag/entries.html",
        title="All {} time entries".format(tag.name),
        now=now,
        events=tag.events,
        total_string=total_string,
        total_decimal=total_decimal,
    )


@bp.route("/default", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def default():
    form = DefaultForm()
    form.tag.choices += [(tag.id, tag.name) for tag in current_user.tags]
    if form.validate_on_submit():
        if form.tag.data == "None":
            current_user.default_tag_id = None
        else:
            current_user.default_tag_id = form.tag.data
        db.session.add(current_user)
        db.session.commit()
        current_app.logger.info("User {} set default tag to {}".format(current_user.id, current_user.default_tag_id))
        flash("Your default tag has been changed.", "success")
        return redirect(url_for("tag.tags"))
    elif request.method == "GET":
        if current_user.default_tag_id:
            form.tag.data = current_user.default_tag_id

    return render_template("tag/default_form.html", title="Default tag", form=form)
