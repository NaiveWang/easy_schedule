import time

from src.todo_keep import keep_daily_refresh

def keep_scheduler():
    while True:
        time.sleep(59)
        print(time.strftime('%H%M'))
        if 0 == int(time.strftime('%H%M')):
            
            keep_daily_refresh()
            time.sleep(61)
