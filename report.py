from apscheduler.schedulers.background import BackgroundScheduler
from my_function.udbotdata import UDBotData

# Instantiate your class
ud_bot_data = UDBotData()

def send_email():
    # Your email sending function here
    ud_bot_data.send_email()
    pass

def send_line():
    # Your line sending function here
    ud_bot_data.send_line_message()
    pass

def main():
    # Existing app.py logic here

    # Initialize your db object
    db = UDBotData()

    for plant, user, password in plant_user_password:
        # Your logic here

    # Start the scheduler
    sched = BackgroundScheduler(daemon=True)

    # Schedule job_every_day to be called every day at 8 o'clock
    sched.add_job(send_email, 'cron', hour=8)

    # Schedule job_every_hour to be called every hour
    sched.add_job(send_line, 'interval', hours=1)

    sched.start()

# Run the main function
if __name__ == "__main__":
    main()
