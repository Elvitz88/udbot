import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from my_function.udbotdata import UDBotData

# โหลดไฟล์ .ini
def load_ini(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

# ดึงข้อมูล plant, user, password, email จากไฟล์ plant_user.ini
def get_plant_data():
    config = load_ini('config.ini')
    plant_data = []
    for section in config.sections():
        if section == 'plant_user':
            for option in config.options(section):
                plant, user, password, email = config.get(section, option).split(',')
                plant_data.append([plant, user, password, email])
    return plant_data

def main():
    # ดึงข้อมูล plant
    plant_data = get_plant_data()

    # Start the scheduler
    sched = BackgroundScheduler(daemon=True)

    # Instantiate your class
    ud_bot_data = UDBotData()

    def report_task_email():
        for plant_info in plant_data:
            plant, user, password, email = plant_info
            ud_bot_data.send_email('email', plant, email)

    def report_task_line():
        for plant_info in plant_data:
            plant, user, password, email = plant_info
            ud_bot_data.send_line('line', plant)

    # Schedule report_task_email to be called every 24 hours
    sched.add_job(report_task_email, 'interval', hours=24)

    # Schedule report_task_line to be called every hour
    sched.add_job(report_task_line, 'interval', hours=1)

    # Start the scheduler
    sched.start()

# Run the main function
if __name__ == "__main__":
    main()
