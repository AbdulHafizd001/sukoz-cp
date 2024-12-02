from flask import Flask
from app.routes.user import bp as user_bp  # Import blueprint 'bp' dari 'user.py'
from app.routes.recipe import recipe_bp 
from app.routes.category import category_bp
from app.routes.rating import rating_bp
from app.routes.bookmark import bookmark_bp
from app import models #bara aja di tambahin 

def create_app():
    app = Flask(__name__)

    app.register_blueprint(user_bp, url_prefix='/api/v1')  # Register blueprint dengan url_prefix
    app.register_blueprint(recipe_bp, url_prefix='/api/v1')
    app.register_blueprint(category_bp, url_prefix='/api/v1')
    app.register_blueprint(rating_bp, url_prefix='/api/v1')
    app.register_blueprint(bookmark_bp, url_prefix='/api/v1')
    return app
