import schedule
import apply
import time


def job() -> None:
    today = time.localtime(time.time())
    print('[Scheduler]', 'Now:', time.asctime(today))
    apply.apply_all()
    print()


schedule.every().day.at('00:05').do(job)
schedule.every().day.at('12:05').do(job)

print('[Scheduler] Started scheduler')
while True:
    schedule.run_pending()
    time.sleep(30)
