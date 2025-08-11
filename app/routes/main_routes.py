from flask import Blueprint, render_template
from app.models.business import Business
from app.models.post import Post
from app.models.request import Request
from app.models.user import User

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    businesses = Business.query.order_by(Business.created_at.desc()).all()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    requests = Request.query.order_by(Request.created_at.desc()).all()
    request_users = {}
    for request in requests:
        request_users[request.id] = User.query.get(request.user_id)
    return render_template('main/homepage.html', businesses=businesses, posts=posts, requests=requests, request_users=request_users)
    
@main.route('/posts')
def posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('main/posts.html', posts=posts)

@main.route('/requests')
def requests():
    requests = Request.query.order_by(Request.created_at.desc()).all()
    request_users = {}
    for request in requests:
        request_users[request.id] = User.query.get(request.user_id)
    return render_template('main/requests.html', requests=requests, request_users=request_users)

@main.route('/businesses')
def businesses():
    businesses = Business.query.order_by(Business.created_at.desc()).all()
    return render_template('main/businesses.html', businesses=businesses)
