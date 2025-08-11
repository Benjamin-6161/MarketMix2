from flask import Blueprint, render_template, redirect, url_for
from app.models.user import User
from app.models.business import Business
from app import db
from flask_login import login_required, current_user

user = Blueprint('user', __name__)

@user.route('/profile')
@login_required
def profile():
    business = Business.query.filter_by(user_id = current_user.id).first()
    has_business = business is not None
    return render_template('user/profile.html', user=current_user, business=business, has_business=has_business)
