from .filter import format_datetime
from flask_login import LoginManager
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app():

    app = Flask(__name__)
    app.config.from_object(config)

    # login manage
    login_manager.init_app(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprint
    from .views import main_views, book_views, review_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(book_views.bp)
    app.register_blueprint(review_views.bp)
    app.register_blueprint(auth_views.bp)

    # filter
    app.jinja_env.filters['datetime'] = format_datetime

    return app
