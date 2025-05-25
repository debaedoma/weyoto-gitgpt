from datetime import datetime, timedelta
from config import Config

def generate_limit_response(logs):
    oldest = logs[0].created_at
    try_again_time = oldest + timedelta(hours=Config.FREE_PLAN_WINDOW_HOURS)

    formatted_time = try_again_time.strftime("%I:%M %p on %b %d").lstrip("0")
    remaining = try_again_time - datetime.utcnow()
    hours_left = remaining.seconds // 3600
    minutes_left = (remaining.seconds % 3600) // 60

    return {
        "error": "You've hit your Free plan limit.",
        "upgrade_cta": "Upgrade for unlimited GitGPT access — just $1/month or $10/year.",
        "upgrade_url": "https://gitgpt.weyoto.com/upgrade",
        "retry_in": f"{hours_left}h {minutes_left}m",
        "try_again_at": formatted_time
    }
