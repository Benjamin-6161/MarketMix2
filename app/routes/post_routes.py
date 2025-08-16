from flask import Blueprint, render_template, redirect, url_for
from app.models.post import Post
from app.models.engagement import Engagement
from app import db
from app.forms import PostForm
from app.forms import EngagementForm
from flask_login import login_required, current_user

post = Blueprint('post', __name__)

@post.route('/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get(post_id)
    form = EngagementForm()
    if form.validate_on_submit():
        engagement = Engagement(
            post_id=post_id,
            user_id=current_user.id,
            engagement_type='comment',
            comment=form.comment.data
        )
        db.session.add(engagement)
        db.session.commit()
        return redirect(url_for('post.post_detail', post_id=post_id))
    return render_template('post/detail.html', post=post, form=form)
    
@post.route('/<int:post_id>/like')
@login_required
def like_post(post_id):
    existing_engagement = Engagement.query.filter_by(post_id=post_id, user_id=current_user.id, engagement_type='like').first()
    if existing_engagement:
        db.session.delete(existing_engagement)
    else:
        engagement = Engagement(
            post_id=post_id,
            user_id=current_user.id,
            engagement_type='like'
        )
        db.session.add(engagement)

    db.session.commit()
    return redirect(url_for('post.post_detail', post_id=post_id))

@post.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if post.business.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post.post_detail', post_id=post_id))
    return render_template('post/edit.html', form=form, post=post)

@post.route('/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return "Post not found", 404
    if post.business is not None and post.business.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('business.business_posts', business_id=post.business_id))
    
@post.route('/<int:post_id>/<int:engagement_id>/delete')
@login_required
def delete_comment(post_id, engagement_id):
    comment = Engagement.query.get(engagement_id)
    if comment and comment.user_id == current_user.id and comment.engagement_type == "comment":
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('post.post_detail', post_id = post_id))