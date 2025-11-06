import random, datetime, json, requests

def analyze_gold():
    # Simulated data — replace with live gold data API if desired
    price = round(random.uniform(2350, 2450), 2)
    direction = random.choice(["BUY", "SELL"])
    atr = 6
    if direction == "BUY":
        sl = round(price - (0.5 * atr), 2)
        tp = round(price + (2 * (price - sl)), 2)
    else:
        sl = round(price + (0.5 * atr), 2)
        tp = round(price - (2 * (sl - price)), 2)

    signal = {
        "timestamp": str(datetime.datetime.utcnow()),
        "pair": "XAU/USD",
        "action": direction,
        "entry": price,
        "stop_loss": sl,
        "take_profit": tp,
        "confidence": f"{random.randint(80,95)}%"
    }

    # Save to JSON
    try:
        with open("signals.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(signal)
    with open("signals.json", "w") as f:
        json.dump(data, f, indent=4)

    # Discord webhook notification
    try:
        discord_webhook = "YOUR_DISCORD_WEBHOOK_URL"
        msg = f"📊 KCFX Signal: {signal['action']} XAU/USD @ {signal['entry']}\nSL: {sl}, TP: {tp}, Confidence: {signal['confidence']}"
        requests.post(discord_webhook, json={"content": msg})
    except:
        pass

    # Telegram bot message
    try:
        telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
        chat_id = "YOUR_CHAT_ID"
        telegram_message = f"📊 KCFX Signal: {signal['action']} XAU/USD\nEntry: {price}\nSL: {sl}\nTP: {tp}\nConfidence: {signal['confidence']}"
        requests.get(f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={chat_id}&text={telegram_message}")
    except:
        pass

    return signal
