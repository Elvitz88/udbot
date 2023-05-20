from my_function.udbot import SAPLoginBot
from my_function.udbotdata import UDBotData
from datetime import datetime
import time

def main():
    plant_user_password=[['A001','user1','pass1'],['A002','user2','pass2']]
    instypes = ['04', '89', '05']
    udbot_data = UDBotData()

    while True:  # Run indefinitely
        for plant_info in plant_user_password:  # Loop over plants and corresponding users and passwords
            plant_code, username, password = plant_info
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

        # Sleep for 5 minutes (300 seconds)
        time.sleep(300)

if __name__ == "__main__":
    main()


