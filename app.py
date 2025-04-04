from flask import Flask
from config import Config
from extensions import db
from Modules.github.routes import github_bp  # We'll define this next

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(github_bp, url_prefix="/query/github")

    return app

# Optional: Allow running directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
