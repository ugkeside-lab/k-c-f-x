import threading, time
from strategy import analyze_gold

def start_scheduler():
    def run():
        while True:
            analyze_gold()
            time.sleep(3600)  # every hour
    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
