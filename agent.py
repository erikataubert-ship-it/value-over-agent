import requests

BOT_TOKEN = "8367507141:AAE-tpC4kKLU8MzJaQncTJS9ailpr23viNY"
CHAT_ID = "8779770443"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

def calc_value(expected_goals, odds):

    # egyszerű Over 2.5 valószínűség becslés
    if expected_goals >= 3.8:
        true_prob = 0.62
    elif expected_goals >= 3.3:
        true_prob = 0.55
    elif expected_goals >= 2.9:
        true_prob = 0.50
    else:
        true_prob = 0.42

    market_prob = 1 / odds

    value = true_prob - market_prob

    return true_prob, market_prob, value

if __name__ == "__main__":

    # TESZT adat
    expected_goals = 3.7
    odds = 2.05

    true_prob, market_prob, value = calc_value(expected_goals, odds)

    if value > 0.05:
        msg = f"""VALUE OVER JELZÉS

Expected Goals: {expected_goals}
Odds: {odds}

Valós esély: {round(true_prob*100,1)}%
Piaci esély: {round(market_prob*100,1)}%

VALUE: {round(value*100,1)}%
"""
        send_telegram(msg)
