from app import db
from .post import Post
from .engagement import Engagement

Post.engagements = db.relationship('Engagement', back_populates='post', lazy=True)
Engagement.post = db.relationship('Post', back_populates='engagements')