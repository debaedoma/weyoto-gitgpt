from datetime import datetime, timedelta
from models.user import RequestLog
from extensions import db
from config import Config

# ✅ This writes down each time the user uses GitGPT
def log_request(user_id, endpoint):
    db.session.add(RequestLog(user_id=user_id, endpoint=endpoint))
    db.session.commit()

# ✅ This checks how many requests the user has made in the last 6 hours
def get_limit_and_logs(user_id, limit=None):
    cutoff = datetime.utcnow() - timedelta(hours=Config.FREE_PLAN_WINDOW_HOURS)
    logs = RequestLog.query.filter(
        RequestLog.user_id == user_id,
        RequestLog.created_at >= cutoff
    ).order_by(RequestLog.created_at.asc()).all()

    return logs, limit or Config.FREE_PLAN_LIMIT