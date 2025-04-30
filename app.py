from flask import Flask
from flask_cors import CORS  # ✅ Added
from config import Config
from extensions import db, migrate
from modules.github.routes import github_bp
from modules.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Allow requests from frontend (local + prod)
    CORS(app, origins=[
        "http://192.168.199.181:3000",                  # Local dev
        "https://frontend url.com"      # Replace with actual frontend prod URL
    ])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(github_bp, url_prefix="/github")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

#Optional to allow running directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
