from flask import Flask
import os
from .extensions import db, login_manager, migrate
from .api import api  # Import the API blueprint for syncing

def create_app():
    app = Flask(__name__)

    # Use environment variables
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret")

    # Set the database URI (PostgreSQL for remote, SQLite for local)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///local.db")  # Default to SQLite locally

    # Disable Flask-SQLAlchemy track modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To avoid overhead

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Set up Flask-Login
    login_manager.login_view = 'auth.login'  # Set the login route to redirect unauthorized users
    login_manager.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Register the API blueprint for syncing data
    app.register_blueprint(api, url_prefix='/api')

    # Import models AFTER db is initialized
    from .models import User, DryingRecord

    # Define user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create the tables using Flask-Migrate (not db.create_all())
    with app.app_context():
        migrate.init_app(app, db)  # Ensure migrations are handled

    return app
