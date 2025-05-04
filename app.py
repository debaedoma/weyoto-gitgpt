from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from modules.github.routes import github_bp
from modules.auth.routes import auth_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Use environment variable to dynamically control CORS origins
    allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")
    CORS(app, origins=allowed_origins)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(github_bp, url_prefix="/github")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
