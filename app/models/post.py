from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
#    image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())