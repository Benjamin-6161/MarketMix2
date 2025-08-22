from flask import Blueprint, render_template, redirect, url_for, current_app
from app.models.user import User
from app.models.request import Request
from app.models.business import Business
from app import db
from app.uploads import profile_photos
from flask_login import login_required, current_user
from app.forms import UserForm

user = Blueprint('user', __name__)

@user.route('/profile')
@login_required
def profile():
    business = Business.query.filter_by(user_id=current_user.id).first()
    has_business = business is not None
    requests = Request.query.filter_by(user_id=current_user.id).all()
    return render_template('user/profile.html', user=current_user, requests=requests, business=business, has_business=has_business, app_config=current_app.config)

@user.route('/<int:user_id>/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    form = UserForm(obj=current_user)
    user = User.query.get(user_id)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.image.data:
            filename = profile_photos.save(form.image.data)
            current_user.image_filename = filename
        db.session.commit()
        return redirect(url_for('user.profile'))
    return render_template('user/edit.html', form=form, user=user)