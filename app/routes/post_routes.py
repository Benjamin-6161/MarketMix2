from flask import Blueprint, render_template, redirect, url_for
from app.models.post import Post
from app import db
from app.forms import PostForm
from flask_login import login_required, current_user

post = Blueprint('post', __name__)

@post.route('/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('post/detail.html', post=post)

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
    if post.business.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('business.business_posts', business_id=post.business_id))