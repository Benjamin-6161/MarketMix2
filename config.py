import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///marketplace.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOADED_IMAGES_DEST = 'app/static/images'
    UPLOADED_PROFILEPHOTOS_DEST = 'app/static/images/profile_photo'
    UPLOADED_BUSINESSPHOTOS_DEST = 'app/static/images/business_photo'
    UPLOADED_POSTIMAGES_DEST = 'app/static/images/posts'
    UPLOADED_REQUESTIMAGES_DEST = 'app/static/images/requests'
    UPLOADED_MESSAGEIMAGES_DEST = 'app/static/images/messages'