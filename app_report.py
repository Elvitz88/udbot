import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from my_function.udbotdata import UDBotData
from datetime import datetime, timedelta

# โหลดไฟล์ .ini
def load_ini(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

# ดึงข้อมูล plant, user, password, email จากไฟล์ plant_user.ini
def get_plant_data():
    config = load_ini('plant_user.ini')
    plant_data = []
    for section in config.sections():
        plant = section
        user = config.get(section, 'user')
        password = config.get(section, 'password')
        email = config.get(section, 'email')
        plant_data.append([plant, user, password, email])
    return plant_data

# ดึงข้อมูล database จากไฟล์ config.ini
def get_db_config():
    config = load_ini('config.ini')
    host = config.get('database', 'host')
    username = config.get('database', 'username')
    password = config.get('database', 'password')
    database = config.get('database', 'database')
    return host, username, password, database

def report_task_email(host, username, password, database):
    # ดึงข้อมูล plant, user, password, email
    plant_data = get_plant_data()

    # Instantiate your class
    ud_bot_data = UDBotData(host, username, password, database)

    for plant, _, _, email in plant_data:
        ud_bot_data.get_and_send_data('email', plant, email)

def report_task_line(host, username, password, database):
    # ดึงข้อมูล plant
    plant_data = get_plant_data()

    # Instantiate your class
    ud_bot_data = UDBotData(host, username, password, database)

    for plant, _, _, _ in plant_data:
        ud_bot_data.get_and_send_data('line', plant)

def main():
    # ดึงข้อมูล database
    host, username, password, database = get_db_config()

    # Start the scheduler
    sched = BackgroundScheduler(daemon=True)

    # Schedule report_task_email to be called every 24 hours
    sched.add_job(report_task_email, 'interval', hours=24, args=[host, username, password, database])

    # Schedule report_task_line to be called every hour
    sched.add_job(report_task_line, 'interval', hours=1, args=[host, username, password, database])

    sched.start()

# Run the main function
if __name__ == "__main__":
    main()