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
            bot.entry_QA32()  # เข้าสู่ระบบ QA32

            for instype in instypes:  # Loop over input types
                bot.information_intlot(plant_code, instype)  # แสดงข้อมูลในหน้า Information from Intlot
                bot.filt_multi_status()  # กำหนดตัวกรองสถานะหลายรายการ

                for _ in range(3):  # Loop for 3 times
                    bot_start = datetime.now()  # เวลาเริ่มต้นการดำเนินการ
                    material, batch, inslot, udcode = bot.inslot_data()  # ดึงข้อมูล InsLot
                    if inslot == '':  # ถ้า InsLot เป็นค่าว่าง
                        break  # ออกจากลูป for _ in range(3)

                    bot.entry_ud()  # เข้าสู่ระบบ UD
                    bot.ud_Char()  # ป้อนข้อมูล UD

                    bot_end = datetime.now()  # เวลาสิ้นสุดการดำเนินการ
                    udbot_data.save_bot_data(bot_start, bot_end, plant_code, material, batch, inslot, udcode)  # บันทึกข้อมูล UD Bot

            bot.close_connection()  # ปิดการเชื่อมต่อกับ SAP

        time.sleep(5)  # หน่วงเวลา 5 วินาที

if __name__ == "__main__":
    main()


    