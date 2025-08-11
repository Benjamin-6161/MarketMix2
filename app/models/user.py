from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    user_type = db.Column(db.String(10), nullable=False, default='customer')  # 'vendor' or 'customer'
    country = db.Column(db.String(50), nullable=False, default='unknown')
    state = db.Column(db.String(50), nullable=False, default='unknown')
    city = db.Column(db.String(50), nullable=False, default='unknown')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    businesses = db.relationship('Business', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)