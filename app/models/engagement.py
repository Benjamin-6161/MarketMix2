from app import db

class Engagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    engagement_type = db.Column(db.String(10), nullable=False)  # 'like', 'comment', 'share'
    comment = db.Column(db.Text, nullable=True)