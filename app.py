from my_function.udbot import SAPLoginBot
from my_function.udbotdata import UDBotData
from datetime import datetime
import time
from configparser import ConfigParser


def get_plant_user_password_email():
    config = ConfigParser()
    config.read('plant_user.ini')

    plant_user_password_email = []
    for section in config.sections():
        plant = section
        user = config.get(section, 'user')
        password = config.get(section, 'password')
        email = config.get(section, 'email')  # การอ่านค่า email
        plant_user_password_email.append([plant, user, password, email])
    
    return plant_user_password_email

def main():
    plant_user_password_email = get_plant_user_password_email()  # การเรียกใช้ function ใหม่
    instypes = ['04', '01', '89']
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
            udbot_data.get_and_send_data('email', plant_code, email)  # การส่ง email หลังจากปิดการเชื่อมต่อ bot

        # Sleep for 5 minutes (300 seconds)
        time.sleep(300)

if __name__ == "__main__":
    main()


