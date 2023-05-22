from my_function.udbot import SAPLoginBot
from my_function.udbotdata import UDBotData
from datetime import datetime
import time
from configparser import ConfigParser


def get_plant_user_password_email():
    config = ConfigParser()
    config.read('config.ini')

    plant_user_password_email = []
    for section in config.sections():
        if section == 'plant_user':
            for option in config.options(section):
                credentials = config.get(section, option).split(',')
                if len(credentials) >= 3:
                    plant = option
                    user = credentials[0]
                    password = credentials[1]
                    email = credentials[2]
                    plant_user_password_email.append([plant, user, password, email])

    return plant_user_password_email

def main():
    plant_user_password_email = get_plant_user_password_email()  # การเรียกใช้ function ใหม่
    instypes = ['89']
    udbot_data = UDBotData()

    while True:  # Run indefinitely
        for plant_info in plant_user_password_email:  # Loop over plants, users, passwords, and emails
            plant_code, username, password, email = plant_info  # การรับค่า email
            bot = SAPLoginBot()
            bot.login(username, password)

            for _ in range(3):  # Loop for 3 times
                for instype in instypes:  # Loop over input types
                    bot_start = datetime.now()  # Get current datetime at the start of the loop
                    bot.entry_QA32()
                    bot.information_intlot(plant_code, instype)  # Use the current plant code and input type
                    bot.change_intlot_data()
                    material, batch, inslot, udcode = bot.inslot_data()
                    bot.ud_Char()
                    bot_end = datetime.now()  # Get current datetime at the end of the loop
                    
                    # Store the data including bot_start and bot_end
                    udbot_data.save_bot_data(bot_start, bot_end, plant_code, material, batch, inslot, udcode)

            bot.close_connection()

        # Sleep for 0.5 minutes (30 seconds)
        time.sleep(30)

if __name__ == "__main__":
    main()


