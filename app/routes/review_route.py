from flask import Blueprint, render_template, redirect, url_for
from app.models.review import Review
from app.models.business import Business
from app import db
from app.forms import ReviewForm
from flask_login import login_required, current_user

review = Blueprint('review', __name__)

@review.route('/business/<int:business_id>/review', methods=['GET', 'POST'])
@login_required
def create_review(business_id):
    business = Business.query.get(business_id)
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(rating=form.rating.data, review=form.review.data, business_id=business_id, user_id=current_user.id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('business.business_profile', business_id=business_id))
    return render_template('review/create.html', form=form, business=business)

@review.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get(review_id)
    if review.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    form = ReviewForm(obj=review)
    if form.validate_on_submit():
        review.rating = form.rating.data
        review.review = form.review.data
        db.session.commit()
        return redirect(url_for('business.business_profile', business_id=review.business_id))
    return render_template('review/edit.html', form=form, review=review)

@review.route('/review/<int:review_id>/delete')
@login_required
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review.user_id != current_user.id:
        return redirect(url_for('main.homepage'))
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('business.business_profile', business_id=review.business_id))