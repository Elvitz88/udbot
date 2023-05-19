
from my_function.udbot import SAPLoginBot

def main():
    plant_codes = ['A001', 'A002', 'A003', 'A004', 'A005', 'A006', 'A007', 'A008', 'A009', 'A011']
    instypes = ['04', '89', '05']
    usernames = ['A', 'B', 'C', 'D', 'E', 'F']
    passwords = ['1', '2', '3', '4', '5', '6']

    for username, password in zip(usernames, passwords):  # Loop over usernames and passwords
        bot = SAPLoginBot()
        bot.login(username, password)

        for plant_code in plant_codes:  # Loop over plant codes
            for _ in range(3):  # Loop for 3 times
                for instype in instypes:  # Loop over input types
                    bot.entry_QA32()
                    bot.information_intlot(plant_code, instype)  # Use the current plant code and input type
                    bot.change_intlot_data()
                    bot.ud_Char()

        bot.close_connection()

if __name__ == "__main__":
    main()
