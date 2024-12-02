#app.register_blueprint(user.bp)
#app.register_blueprint(recipe.bp)
#app.register_blueprint(category.bp)
#app.register_blueprint(rating.bp)
#app.register_blueprint(bookmark.bp)

from app.routes import user, recipe, category, rating, bookmark
from app.routes.category import category_bp

# Register blueprints
app.register_blueprint(user.bp, url_prefix='/api/v1')
app.register_blueprint(recipe.bp, url_prefix='/api/v1')
app.register_blueprint(category.bp, url_prefix='/api/v1')
app.register_blueprint(rating.bp, url_prefix='/api/v1')
app.register_blueprint(bookmark.bp, url_prefix='/api/v1')