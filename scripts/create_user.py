from app import create_app
from extensions import db
from models.user import User

app = create_app()

with app.app_context():
    user = User(email="te@weyoto.com")
    db.session.add(user)
    db.session.commit()
    print("✅ User created. API Key:", user.api_key)
