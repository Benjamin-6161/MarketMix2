from flask import Blueprint, render_template, redirect, url_for, request, current_app
from app.models.message import Message
from app.models.user import User
from app import db
from app.uploads import message_images
from app.forms import MessageForm
from flask_login import login_required, current_user

message = Blueprint('message', __name__)

@message.route('/inbox')
@login_required
def inbox():
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) | (Message.recipient_id == current_user.id)
    ).order_by(Message.created_at.desc()).all()
    conversation_partners = {}
    for message in messages:
        if message.sender_id == current_user.id:
            partner_id = message.recipient_id
        else:
            partner_id = message.sender_id
        if partner_id not in conversation_partners:
            conversation_partners[partner_id] = message
    partners = []
    for partner_id, message in conversation_partners.items():
        partner = User.query.get(partner_id)
        partners.append((partner, message))
    return render_template('message/inbox.html', conversation_partners=partners, app_config=current_app.config)

@message.route('/message/<int:user_id>')
@login_required
def view_conversation(user_id):
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    partner = User.query.get(user_id)
    return render_template('message/detail.html', messages=messages, partner=partner)

@message.route('/message/send', methods=['GET', 'POST'])
@login_required
def send_message():
    form = MessageForm()
    if form.validate_on_submit():
        new_message = Message(content=form.content.data, recipient_id=form.recipient_id.data, sender_id=current_user.id)
        if form.image.data:
            filename = message_images.save(form.image.data)
            new_message.image_filename = filename
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('message.inbox'))
    return render_template('message/send.html', form=form)

@message.route('/message/send/<int:recipient_id>', methods=['POST'])
@login_required
def send_message_to_user(recipient_id):
    content = request.form.get('content')
    new_message = Message(content=content, recipient_id=recipient_id, sender_id=current_user.id)
    if 'image' in request.files:
        image = request.files['image']
        filename = message_images.save(image)
        new_message.image_filename = filename
    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('message.view_conversation', user_id=recipient_id))