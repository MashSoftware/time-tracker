from datetime import datetime

import pytz
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, fresh_login_required, login_required
from werkzeug.exceptions import Forbidden

from app import csrf, db, limiter
from app.location import bp
from app.location.forms import DefaultForm, LocationForm
from app.models import Location
from app.utils import seconds_to_decimal, seconds_to_string


@bp.route("/")
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def locations():
    now = pytz.utc.localize(datetime.utcnow())
    for location in current_user.locations:
        total_seconds = 0
        for event in location.events:
            total_seconds += event.duration(end=now)

        location.total_string = seconds_to_string(total_seconds)
        location.total_decimal = seconds_to_decimal(total_seconds)

    return render_template("locations.html", title="Locations")


@bp.route("/new", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def create():
    if len(current_user.locations) == current_user.location_limit:
        flash(
            "You have reached the {0} location limit for your account. "
            "Please delete an existing location in order to create a new one.".format(current_user.location_limit),
            "info",
        )
        return redirect(url_for("location.locations"))
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(user_id=current_user.id, name=form.name.data.strip())
        db.session.add(location)
        db.session.commit()
        current_app.logger.info("User {} created location {}".format(current_user.id, location.id))
        flash("Location has been created.", "success")
        return redirect(url_for("location.locations"))
    return render_template("create_location_form.html", title="Create location", form=form)


@bp.route("/<uuid:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def update(id):
    location = Location.query.get_or_404(str(id), description="Location not found")
    if location not in current_user.locations:
        raise Forbidden()
    form = LocationForm()
    if form.validate_on_submit():
        location.name = form.name.data.strip()
        location.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(location)
        db.session.commit()
        current_app.logger.info("User {} updated location {}".format(current_user.id, location.id))
        flash("Location has been saved.", "success")
        return redirect(url_for("location.locations"))
    elif request.method == "GET":
        form.name.data = location.name
    return render_template("update_location_form.html", title="Edit location", form=form, location=location)


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
@csrf.exempt
@fresh_login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def delete(id):
    location = Location.query.get_or_404(str(id), description="Location not found")
    if location not in current_user.locations:
        raise Forbidden()
    if request.method == "GET":
        now = pytz.utc.localize(datetime.utcnow())
        total_seconds = 0
        for event in location.events:
            total_seconds += event.duration(end=now)

        location.total_string = seconds_to_string(total_seconds)
        location.total_decimal = seconds_to_decimal(total_seconds)

        return render_template("delete_location.html", title="Delete location", location=location)
    elif request.method == "POST":
        current_app.logger.info("User {} deleted location {}".format(current_user.id, location.id))
        db.session.delete(location)
        db.session.commit()
        flash("Location has been deleted.", "success")
        return redirect(url_for("location.locations"))


@bp.route("/<uuid:id>/entries", methods=["GET"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def entries(id):
    location = Location.query.get_or_404(str(id), description="Location not found")
    if location not in current_user.locations:
        raise Forbidden()
    now = pytz.utc.localize(datetime.utcnow())

    total_seconds = 0
    for event in location.events:
        total_seconds += event.duration(end=now)

    total_string = seconds_to_string(total_seconds)
    total_decimal = seconds_to_decimal(total_seconds)

    return render_template(
        "entries.html",
        title="All {} time entries".format(location.name),
        now=now,
        events=location.events,
        total_string=total_string,
        total_decimal=total_decimal,
    )


@bp.route("/default", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def default():
    form = DefaultForm()
    form.location.choices += [(location.id, location.name) for location in current_user.locations]
    if form.validate_on_submit():
        if form.location.data == "None":
            current_user.default_location_id = None
        else:
            current_user.default_location_id = form.location.data
        db.session.add(current_user)
        db.session.commit()
        current_app.logger.info(
            "User {} set default location to {}".format(current_user.id, current_user.default_location_id)
        )
        flash("Your default location has been changed.", "success")
        return redirect(url_for("location.locations"))
    elif request.method == "GET":
        if current_user.default_location_id:
            form.location.data = str(current_user.default_location_id)

    return render_template("default_location_form.html", title="Default location", form=form)
