from app import create_app
from extensions import db
from models.user import User
from utils.encryption import encrypt_token

app = create_app()

with app.app_context():
    users = User.query.all()
    for u in users:
        if u.github_pat and not u.github_pat.startswith("gAAAA"):
            u.github_pat = encrypt_token(u.github_pat)
        if u.github_token and not u.github_token.startswith("gAAAA"):
            u.github_token = encrypt_token(u.github_token)
    db.session.commit()
    print("✅ Migration complete: tokens encrypted.")
