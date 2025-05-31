from flask import Flask,jsonify
from flask_cors import CORS
from config import Config
from extensions import db, migrate
from modules.github.routes import github_bp
from modules.auth.routes import auth_bp
from modules.billing.routes import billing_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Friendly homepage/status route
    @app.route("/")
    def status():
        return jsonify({
            "status": "Hello, how are you doing today? Do you like our tool? We'd love to hear from you: hello@weyoto.com",
            "version": "MVP",
            "routes": ["/github/query", "/auth", "/billing"]
        })

    # ✅ Use environment variable to dynamically control CORS origins
    allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")
    CORS(app, origins=allowed_origins)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(github_bp, url_prefix="/github")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(billing_bp, url_prefix="/billing")

    if Config.ENABLE_GITHUB_OAUTH:
        from modules.auth.github_oauth_routes import github_oauth_bp
        app.register_blueprint(github_oauth_bp, url_prefix="/auth")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
