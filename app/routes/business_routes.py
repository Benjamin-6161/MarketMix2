from flask import Blueprint, render_template, redirect, url_for, current_app
from app.models.business import Business
from app.models.post import Post
from app.models.review import Review
from app.models.user import User
from app import db
from app.uploads import business_photos, post_images
from app.forms import BusinessForm, PostForm
from flask_login import login_required, current_user

business = Blueprint('business', __name__)

@business.route('/<int:business_id>')
def business_profile(business_id):
    business = Business.query.get(business_id)
    posts = Post.query.filter_by(business_id=business_id).all()
    reviews = Review.query.filter_by(business_id=business_id).all()
    review = Review.query.filter_by(business_id=business_id, user_id=current_user.id).first()
    has_reviewed = review is not None
    for review in reviews:
        user = User.query.get(review.user_id)
    return render_template('business/profile.html', business=business, posts=posts, reviews=reviews, has_reviewed=has_reviewed, app_config=current_app.config)

@business.route('/<int:business_id>/posts')
def business_posts(business_id):
    posts = Post.query.filter_by(business_id=business_id).all()
    business = Business.query.get(business_id)
    return render_template('business/post.html', posts=posts, business=business, app_config=current_app.config)

@business.route('/create', methods=['GET', 'POST'])
@login_required
def create_business():
    form = BusinessForm()
    if form.validate_on_submit():
        business = Business(
            user_id=current_user.id,
            business_name=form.name.data,
            category=form.category.data,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            description=form.description.data
        )
        if form.image.data:
            filename = business_photos.save(form.image.data)
            business.image_filename = filename
        db.session.add(business)
        db.session.commit()
        return redirect(url_for('business.business_profile', business_id=business.id))
    return render_template('business/create.html', form=form)

@business.route('/<int:business_id>/post/create', methods=['GET', 'POST'])
@login_required
def create_post(business_id):
    form = PostForm()
    from app.models.business import Business
    business = Business.query.get(business_id)
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, business_id=business_id)
        if form.image.data:
            filename = post_images.save(form.image.data)
            new_post.image_filename = filename
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.homepage'))
    return render_template('post/create.html', form=form, business=business)

@business.route('/<int:business_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_business(business_id):
    business = Business.query.get(business_id)
    if business.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    form = BusinessForm(obj=business)
    if form.validate_on_submit():
        business.business_name = form.name.data
        business.category = form.category.data
        business.country = form.country.data
        business.state = form.state.data
        business.city = form.city.data
        business.description = form.description.data
        if form.image.data:
            filename = business_photos.save(form.image.data)
            business.image_filename = filename
        db.session.commit()
        return redirect(url_for('business.business_profile', business_id=business_id))
    return render_template('business/edit.html', form=form, business=business)

@business.route('/<int:business_id>/delete')
@login_required
def delete_business(business_id):
    business = Business.query.get(business_id)
    if business.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    db.session.delete(business)
    db.session.commit()
    return redirect(url_for('main.homepage'))