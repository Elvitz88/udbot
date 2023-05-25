from my_function.udbot_v2 import SAPLoginBot
from my_function.udbotdata import UDBotData
from datetime import datetime
import time
from configparser import ConfigParser

def get_plant_user_password_email():
    config = ConfigParser()
    config.read('config.ini')

    plant_user_password_email = []
    # วน loop ทุก section ใน config file
    for section in config.sections():
        # ตรวจสอบว่า section ปัจจุบันเป็น 'plant_user' หรือไม่
        if section == 'plant_user':
            # วน loop ทุก option ใน section นี้
            for option in config.options(section):
                credentials = config.get(section, option).split(',')
                # ตรวจสอบว่า credentials มีจำนวน 3 ตัวขึ้นไปหรือไม่ (user, password, email)
                if len(credentials) >= 3:
                    plant = option
                    user = credentials[0]
                    password = credentials[1]
                    email = credentials[2]
                    # จัดเก็บ plant, user, password, email ใน list
                    plant_user_password_email.append([plant, user, password, email])

    return plant_user_password_email

def main():
    # เรียกใช้ฟังก์ชันเพื่อรับข้อมูล plant, user, password, email
    plant_user_password_email = get_plant_user_password_email()  
    instypes = ['89']
    udbot_data = UDBotData()

    # รันโค้ดอย่างต่อเนื่อง
    while True:  
        # วน loop ทุก plant, user, password, email
        for plant_info in plant_user_password_email:  
            # แยกข้อมูล plant code, username, password, email
            plant_code, username, password, email = plant_info  
            bot = SAPLoginBot()
            # ล็อกอินเข้าสู่ระบบ SAP
            bot.login(username, password)

            # วน loop ทุก inspection type
            for instype in instypes:  
                # เข้าสู่ QA32 transaction
                bot.entry_QA32()
                # กรอกข้อมูล plant code และ inspection type
                bot.information_intlot(plant_code, instype)  
                # ประมวลผลแถวข้อมูล
                bot.process_rows()
                # ดำเนินการ user decision
                bot.ud_step(plant_code)

            # ปิดการเชื่อมต่อกับ SAP
            bot.close_connection()
        # หยุดเวลา 30 วินาที
        time.sleep(30)

# รันโค้ดหลัก
if __name__ == "__main__":
    main()
