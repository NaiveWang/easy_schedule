import time

from src.todo_keep import keep_daily_refresh

def keep_scheduler():
    while True:
        time.sleep(59)
        if 0 == int(time.strftime('%H%M')):
            #print(time.strftime('%H%M'))
            time.sleep(61)
            keep_daily_refresh()
