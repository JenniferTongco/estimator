import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize the database and migration tools
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Set the secret key for security purposes
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")

    # Set up the database URI (PostgreSQL for the remote app, SQLite for local)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///local.db")  # Default to SQLite locally

    # Prevent Flask-SQLAlchemy from tracking modifications (to save resources)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with the database
    db.init_app(app)
    migrate.init_app(app, db)

    # Register the blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models and set up Flask-Login
    from .models import User, DryingRecord
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to login if user is not authenticated
    login_manager.init_app(app)

    # Define the user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create all tables (only needed if you're not using migrations)
    with app.app_context():
        db.create_all()

    return app
