from datetime import date, datetime, timedelta

import pytz
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, fresh_login_required, login_required
from werkzeug.exceptions import Forbidden

from app import csrf, db, limiter
from app.entry import bp
from app.entry.forms import EventForm
from app.models import Event
from app.utils import seconds_to_decimal, seconds_to_string


@bp.route("/")
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def weekly():
    if len(current_user.tags) == 0:
        flash(
            "You need to <a href='{0}' class='alert-link'>create a new tag</a> to start categorising your time entries.".format(
                url_for("tag.create")
            ),
            "info",
        )

    if current_user.schedule() == 0:
        flash(
            "You need to <a href='{0}' class='alert-link'>set your scheduled time</a> to start tracking weekly progress.".format(
                url_for("account.schedule")
            ),
            "info",
        )

    now = pytz.utc.localize(datetime.utcnow())
    today = date.today().isocalendar()
    year = request.args.get("year", default=str(today[0]), type=str)
    week = request.args.get("week", default=str(today[1]), type=str)
    first_day = datetime.strptime(year + week + "1", "%G%V%u")
    last_day = datetime.strptime(year + week + "7", "%G%V%u")
    next_week = (first_day + timedelta(weeks=1)).isocalendar()
    previous_week = (first_day - timedelta(weeks=1)).isocalendar()

    last_event = Event.query.filter_by(user_id=current_user.id).order_by(Event.started_at.desc()).first()
    if (last_event and last_event.ended_at) or last_event is None:
        start = True
    else:
        start = False

    if first_day.strftime("%Y") == last_day.strftime("%Y"):
        if first_day.strftime("%B") == last_day.strftime("%B"):
            title = first_day.strftime("%d") + " to " + last_day.strftime("%d %B %Y")
        else:
            title = first_day.strftime("%d %B") + " to " + last_day.strftime("%d %B %Y")
    else:
        title = first_day.strftime("%d %B %Y") + " to " + last_day.strftime("%d %B %Y")

    events = (
        Event.query.filter_by(user_id=current_user.id)
        .filter(Event.started_at.between(first_day, last_day))
        .order_by(Event.started_at.desc())
        .all()
    )

    weekly_seconds = 0
    for event in events:
        event.started_at = event.started_at.astimezone(pytz.timezone(current_user.timezone))
        if event.ended_at:
            event.ended_at = event.ended_at.astimezone(pytz.timezone(current_user.timezone))
        weekly_seconds += event.duration(end=now)

    weekly_string = seconds_to_string(weekly_seconds) if weekly_seconds > 0 else None
    weekly_decimal = seconds_to_decimal(weekly_seconds)

    if weekly_seconds < current_user.schedule():
        weekly_delta = current_user.schedule() - weekly_seconds
    else:
        weekly_delta = weekly_seconds - current_user.schedule()

    weekly_delta_string = seconds_to_string(weekly_delta)
    weekly_delta_decimal = seconds_to_decimal(weekly_delta)

    if current_user.schedule():
        progress = int((weekly_seconds / current_user.schedule()) * 100)
    else:
        progress = 0

    tag_totals = []
    for tag in current_user.tags:
        tag_total = {"total": 0}
        for event in events:
            if tag.id == event.tag_id:
                tag_total["name"] = tag.name
                tag_total["total"] += event.duration(end=now)
        if tag_total["total"] > 0:
            tag_total["decimal"] = seconds_to_decimal(tag_total["total"])
            tag_total["total"] = seconds_to_string(tag_total["total"])
            tag_totals.append(tag_total)

    location_totals = []
    for location in current_user.locations:
        location_total = {"total": 0}
        for event in events:
            if location.id == event.location_id:
                location_total["name"] = location.name
                location_total["total"] += event.duration(end=now)
        if location_total["total"] > 0:
            location_total["decimal"] = seconds_to_decimal(location_total["total"])
            location_total["total"] = seconds_to_string(location_total["total"])
            location_totals.append(location_total)

    return render_template(
        "weekly.html",
        now=now,
        start=start,
        today=today,
        next_week=next_week,
        previous_week=previous_week,
        events=events,
        weekly_string=weekly_string,
        weekly_decimal=weekly_decimal,
        weekly_delta_string=weekly_delta_string,
        weekly_delta_decimal=weekly_delta_decimal,
        progress=progress,
        tag_totals=tag_totals,
        location_totals=location_totals,
        title=title,
    )


@bp.route("/auto")
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def auto():
    event = Event.query.filter_by(user_id=current_user.id).order_by(Event.started_at.desc()).first()
    if event and event.ended_at is None:
        event.ended_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(event)
        current_app.logger.info("User {} stopped entry {}".format(current_user.id, event.id))
    else:
        event = Event(user_id=current_user.id, started_at=pytz.utc.localize(datetime.utcnow()))

        if request.args.get("tag_id", None, type=str):
            event.tag_id = request.args.get("tag_id", None, type=str)
        else:
            event.tag_id = current_user.default_tag_id

        if current_user.default_location_id:
            event.location_id = current_user.default_location_id

        db.session.add(event)
        current_app.logger.info("User {} started entry {} with tag {}".format(current_user.id, event.id, event.tag_id))
    db.session.commit()
    return redirect(url_for("entry.weekly"))


@bp.route("/manual", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def manual():
    form = EventForm()
    form.tag.choices += [(tag.id, tag.name) for tag in current_user.tags]
    form.location.choices += [(location.id, location.name) for location in current_user.locations]
    if form.validate_on_submit():
        started_at = datetime(
            form.started_at_date.data.year,
            form.started_at_date.data.month,
            form.started_at_date.data.day,
            form.started_at_time.data.hour,
            form.started_at_time.data.minute,
            form.started_at_time.data.second,
        )
        locale_started_at = pytz.timezone(current_user.timezone).localize(started_at)
        utc_started_at = locale_started_at.astimezone(pytz.utc)
        event = Event(user_id=current_user.id, started_at=utc_started_at)
        if form.ended_at_date.data and form.ended_at_time.data:
            ended_at = datetime(
                form.ended_at_date.data.year,
                form.ended_at_date.data.month,
                form.ended_at_date.data.day,
                form.ended_at_time.data.hour,
                form.ended_at_time.data.minute,
                form.ended_at_time.data.second,
            )
            locale_ended_at = pytz.timezone(current_user.timezone).localize(ended_at)
            utc_ended_at = locale_ended_at.astimezone(pytz.utc)
            event.ended_at = utc_ended_at
        else:
            event.ended_at = None
        if form.tag.data != "None":
            event.tag_id = form.tag.data
        if form.location.data != "None":
            event.location_id = form.location.data
        if len(form.comment.data.strip()) == 0:
            event.comment = None
        else:
            event.comment = form.comment.data.strip()
        db.session.add(event)
        db.session.commit()
        current_app.logger.info(
            "User {} created entry {} with tag {} in location {}".format(
                current_user.id, event.id, event.tag_id, event.location_id
            )
        )
        flash("Time entry has been added.", "success")
        return redirect(url_for("entry.weekly"))
    elif request.method == "GET":
        if current_user.default_tag_id is None:
            form.tag.data = "None"
        else:
            form.tag.data = current_user.default_tag_id

        if current_user.default_location_id is None:
            form.location.data = "None"
        else:
            form.location.data = current_user.default_location_id
    return render_template("create_entry_form.html", title="Create time entry", form=form)


@bp.route("/<uuid:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def update(id):
    event = Event.query.get_or_404(str(id), description="Time entry not found")
    if event not in current_user.events:
        raise Forbidden()
    form = EventForm()
    form.tag.choices += [(tag.id, tag.name) for tag in current_user.tags]
    form.location.choices += [(location.id, location.name) for location in current_user.locations]
    if form.validate_on_submit():
        started_at = datetime(
            form.started_at_date.data.year,
            form.started_at_date.data.month,
            form.started_at_date.data.day,
            form.started_at_time.data.hour,
            form.started_at_time.data.minute,
            form.started_at_time.data.second,
        )
        locale_started_at = pytz.timezone(current_user.timezone).localize(started_at)
        utc_started_at = locale_started_at.astimezone(pytz.utc)
        event.started_at = utc_started_at
        if form.ended_at_date.data and form.ended_at_time.data:
            ended_at = datetime(
                form.ended_at_date.data.year,
                form.ended_at_date.data.month,
                form.ended_at_date.data.day,
                form.ended_at_time.data.hour,
                form.ended_at_time.data.minute,
                form.ended_at_time.data.second,
            )
            locale_ended_at = pytz.timezone(current_user.timezone).localize(ended_at)
            utc_ended_at = locale_ended_at.astimezone(pytz.utc)
            event.ended_at = utc_ended_at
        else:
            event.ended_at = None

        if form.tag.data != "None":
            event.tag_id = form.tag.data
        else:
            event.tag_id = None

        if form.location.data != "None":
            event.location_id = form.location.data
        else:
            event.location_id = None

        if len(form.comment.data.strip()) == 0:
            event.comment = None
        else:
            event.comment = form.comment.data.strip()
        db.session.add(event)
        db.session.commit()
        current_app.logger.info("User {} updated entry {} with tag {}".format(current_user.id, event.id, event.tag_id))
        flash("Time entry changes have been saved.", "success")
        return redirect(url_for("entry.weekly"))
    elif request.method == "GET":
        # Show timestamp in users localised timezone
        form.started_at_date.data = event.started_at.astimezone(pytz.timezone(current_user.timezone))
        form.started_at_time.data = event.started_at.astimezone(pytz.timezone(current_user.timezone))
        if event.ended_at:
            form.ended_at_date.data = event.ended_at.astimezone(pytz.timezone(current_user.timezone))
            form.ended_at_time.data = event.ended_at.astimezone(pytz.timezone(current_user.timezone))

        if event.tag_id is None:
            form.tag.data = "None"
        else:
            form.tag.data = event.tag_id

        if event.location_id is None:
            form.location.data = "None"
        else:
            form.location.data = event.location_id

        form.comment.data = event.comment
    return render_template("update_entry_form.html", title="Edit time entry", form=form, event=event)


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
@csrf.exempt
@fresh_login_required
@limiter.limit("2 per second", key_func=lambda: current_user.id)
def delete(id):
    event = Event.query.get_or_404(str(id), description="Time entry not found")
    if event not in current_user.events:
        raise Forbidden()

    now = pytz.utc.localize(datetime.utcnow())

    if request.method == "GET":
        return render_template("delete_entry.html", title="Delete time entry", event=event, now=now)
    elif request.method == "POST":
        current_app.logger.info(
            "User {} deleted entry {} with tag {} in location {}".format(
                current_user.id, event.id, event.tag_id, event.location_id
            )
        )
        db.session.delete(event)
        db.session.commit()
        flash("Time entry has been deleted.", "success")
        return redirect(url_for("entry.weekly"))
