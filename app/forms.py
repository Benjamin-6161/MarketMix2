from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message = 'Passwords must match')])
    user_type = SelectField('User Type', choices=[('customer', 'Customer'), ('vendor', 'Vendor')], validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class BusinessForm(FlaskForm):
    name = StringField('Business Name', validators=[DataRequired()])
    category = SelectField('Business Category', choices=[('sales', 'Sales'), ('service', 'Service'),('other','Other')], validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    description = TextAreaField('Business Description')
    submit = SubmitField('Create Business')

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    content = TextAreaField('Post Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Create Review')

class MessageForm(FlaskForm):
    content = TextAreaField('Message Content', validators=[DataRequired()])
    recipient_id = IntegerField('Recipient ID', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class RequestForm(FlaskForm):
    category = SelectField('Category', choices=[('service', 'Service'), ('business', 'Business')], validators=[DataRequired()])
    content = TextAreaField('Request Content', validators=[DataRequired()])
    submit = SubmitField('Create Request')