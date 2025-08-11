from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    with app.app_context():
        
        db.create_all()

    from .routes.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .routes.main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.user_routes import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .routes.business_routes import business as business_blueprint
    app.register_blueprint(business_blueprint, url_prefix='/business')

    from .routes.post_routes import post as post_blueprint
    app.register_blueprint(post_blueprint, url_prefix='/post')

    from .routes.review_route import review as review_blueprint
    app.register_blueprint(review_blueprint)

    from .routes.message_routes import message as message_blueprint
    app.register_blueprint(message_blueprint, url_prefix='/message')

    from .routes.request_routes import request as request_blueprint
    app.register_blueprint(request_blueprint, url_prefix='/request')

    return app