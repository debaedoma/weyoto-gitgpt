# scripts/init_db.py

from app import create_app
from extensions import db
from models.user import User  # Add other models here as you grow

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
