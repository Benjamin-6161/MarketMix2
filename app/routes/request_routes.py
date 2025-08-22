from flask import Blueprint, render_template, redirect, url_for, current_app
from app.models.request import Request
from app.models.user import User
from app import db
from app.uploads import request_images
from app.forms import RequestForm
from flask_login import login_required, current_user

request = Blueprint('request', __name__)

@request.route('/create', methods=['GET', 'POST'])
@login_required
def create_request():
    form = RequestForm()
    if form.validate_on_submit():
        new_request = Request(
            category=form.category.data,
            content=form.content.data,
            user_id=current_user.id
        )
        if form.image.data:
            filename = request_images.save(form.image.data)
            new_request.image_filename = filename
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('main.homepage'))
    return render_template('request/create.html', form=form)

@request.route('/<int:request_id>')
@login_required
def view_request(request_id):
    request_obj = Request.query.get(request_id)
    return render_template('request/detail.html', request=request_obj, user=request_obj.user, app_config=current_app.config)

@request.route('/<int:request_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    request_obj = Request.query.get(request_id)
    if request_obj.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    form = RequestForm(obj=request_obj)
    if form.validate_on_submit():
        request_obj.category = form.category.data
        request_obj.content = form.content.data
        db.session.commit()
        return redirect(url_for('request.view_request', request_id=request_id))
    return render_template('request/edit.html', form=form, request=request_obj)

@request.route('/<int:request_id>/delete')
@login_required
def delete_request(request_id):
    request_obj = Request.query.get(request_id)
    if request_obj.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    db.session.delete(request_obj)
    db.session.commit()
    return redirect(url_for('main.homepage'))
    