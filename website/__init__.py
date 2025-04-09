from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_migrate import Migrate  # Import Flask-Migrate for handling migrations
from .api import api  # Import the API blueprint for syncing

# Initialize the database (only the instance)
db = SQLAlchemy()
migrate = Migrate()  # Initialize Flask-Migrate

def create_app():
    app = Flask(__name__)

    # Use environment variables
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")

    # Set the database URI (PostgreSQL for remote, SQLite for local)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///local.db")  # Default to SQLite locally

    # Disable Flask-SQLAlchemy track modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid overhead

    # Initialize the app with the database
    db.init_app(app)  # Initialize db with app here

    # Initialize Flask-Migrate with the app and database
    migrate.init_app(app, db)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Register the API blueprint for syncing data
    app.register_blueprint(api, url_prefix='/api')

    # Import models
    from .models import User, DryingRecord

    # Set up Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login route to redirect unauthorized users
    login_manager.init_app(app)

    # Define user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create all tables (initial setup) - Only for SQLite or PostgreSQL when no migration is set
    with app.app_context():
        db.create_all()  # Ensures db creation

    return app
