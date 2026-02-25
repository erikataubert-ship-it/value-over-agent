import requests
import os
import json
from datetime import datetime

API_KEY = os.getenv("RAPIDAPI_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CACHE_FILE = "sent_matches.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_cache(match_id):
    cache = load_cache()
    cache.append(match_id)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache[-50:], f)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def dynamic_probability(minute, home_score, away_score):
    base = 0.55
    goal_factor = (home_score + away_score) * 0.05
    time_factor = (minute / 15) * 0.1
    return min(0.85, base + goal_factor + time_factor)

def run_agent():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] E-Football LIVE keresés...")

    url = "https://flashscore4.p.rapidapi.com/v2/matches/live"
    querystring = {"sport_id":"1"}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "flashscore4.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers, params=querystring)
    print("STATUS:", r.status_code)

    if r.status_code != 200:
        print("API hiba")
        return

    data = r.json()

    if not isinstance(data, dict):
        return

    sent_cache = load_cache()

    for event in data.get("DATA", []):
        if not isinstance(event, dict):
            continue

        if "E-Football" not in str(event.get("tournament", {}).get("name","")):
            continue

        match_id = str(event.get("id"))

        if match_id in sent_cache:
            continue

        minute = int(event.get("time", {}).get("minute", 0))
        home_score = int(event.get("homeScore", 0))
        away_score = int(event.get("awayScore", 0))

        prob = dynamic_probability(minute, home_score, away_score)
        odds = 1.85

        value = prob * odds - 1

        if value > 0.03:
            msg = f"""
🔥 E-Football VALUE

⚽ {event.get('home',{}).get('name')} vs {event.get('away',{}).get('name')}
⏱️ {minute}'
📊 Score: {home_score}-{away_score}

📈 Value: {round(value,3)}
"""
            send_telegram(msg)
            save_to_cache(match_id)

run_agent()
