from datetime import datetime

import pytz
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.exceptions import Forbidden

from app import db, limiter
from app.models import Tag
from app.tag import bp
from app.tag.forms import TagForm


@bp.route('/')
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def tags():
    tags = Tag.query.filter_by(user_id=current_user.id).order_by(Tag.name.asc())
    return render_template('tag/tags.html', title='Tags', tags=tags)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def create():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(user_id=current_user.id, name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash('Tag has been created.', 'success')
        return redirect(url_for('tag.tags'))
    return render_template('tag/create_tag_form.html', title='Create tag', form=form)


@bp.route('/<uuid:id>', methods=['GET', 'POST'])
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def update(id):
    tag = Tag.query.get_or_404(str(id))
    if tag not in current_user.tags:
        raise Forbidden()
    form = TagForm()
    if form.validate_on_submit():
        tag.name = form.name.data
        tag.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(tag)
        db.session.commit()
        flash('Tag has been updated.', 'success')
        return redirect(url_for('tag.tags'))
    elif request.method == 'GET':
        form.name.data = tag.name
    return render_template('tag/update_tag_form.html', title='Edit tag', form=form, tag=tag)


@bp.route('/<uuid:id>/delete')
@login_required
@limiter.limit("1 per second", key_func=lambda: current_user.id)
def delete(id):
    tag = Tag.query.get_or_404(str(id))
    if tag not in current_user.tags:
        raise Forbidden()
    db.session.delete(tag)
    db.session.commit()
    flash('Tag has been deleted.', 'success')
    return redirect(url_for('tag.tags'))
