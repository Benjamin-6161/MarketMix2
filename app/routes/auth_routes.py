from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from app.models.user import User
from app import db, profile_photos
from passlib.hash import bcrypt
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(f"User: {user}")
        print(f"Email:{user.email}")
        print(f"Password: {user.password}")
        if user and bcrypt.verify(form.password.data, user.password):
            login_user(user)
            print("Login successful")
            return redirect(url_for('main.homepage'))
        else:
            print("Login failed")
            flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            user_type=form.user_type.data,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            is_active=True
        )
        if form.image.data:
            filename = profile_photos.save(form.image.data)
            new_user.image_filename = filename
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Send password reset email logic here
            flash('Password reset email sent', 'success')
        else:
            flash('Email not found', 'danger')
    return render_template('auth/forgot_password.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Reset password logic here
        flash('Password reset successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))