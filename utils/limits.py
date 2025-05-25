from datetime import datetime, timedelta
from config import Config

def generate_limit_response(try_again_time):
    remaining = try_again_time - datetime.utcnow()
    hours_left = remaining.seconds // 3600
    minutes_left = (remaining.seconds % 3600) // 60

    return {
        "error": "You've hit your Free plan limit.",
        "upgrade_cta": "Upgrade for unlimited GitGPT access — just $1/month or $10/year.",
        "upgrade_url": "https://gitgpt.weyoto.com/upgrade",
        "retry_in": f"{hours_left}h {minutes_left}m",
    }
