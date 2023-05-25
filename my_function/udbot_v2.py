import pyautogui
import pyperclip
import time
import cv2
import os
import json
import numpy as np
from datetime import datetime, timedelta
from my_function.udbotdata import UDBotData

def safe_sleep(duration):
    '''A wrapper function for time.sleep()'''
    time.sleep(duration)

class SAPLoginBot:
    
    def __init__(self):
        self.udbot_data = UDBotData()

        project_dir = os.path.dirname(__file__)  # gets directory where the python script is located
        picture_dir = os.path.join(project_dir, 'documents', 'pictures')  # creates the path to the 'pictures' folder

        self.sap_icon_logo = os.path.join(picture_dir, 'saplogo.png')
        self.systemlogin_icon = os.path.join(picture_dir, 'Systemlogin.png')
        self.statusud_icon = os.path.join(picture_dir, 'StatusUD.png')
        self.chagelongtextud_icon = os.path.join(picture_dir, 'changelongtextUD3.png')

        self.username_field_location = (229, 206)
        self.password_field_location = (214, 230)
        self.login_button_location = (600, 600)

    def login(self, username, password): 
        try:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            image_template = cv2.imread(self.sap_icon_logo)
            result = cv2.matchTemplate(screenshot, image_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            image_height, image_width, _ = image_template.shape
            center_x = max_loc[0] + image_width // 2
            center_y = max_loc[1] + image_height // 2
            pyautogui.moveTo(center_x, center_y)
            pyautogui.doubleClick()
            safe_sleep(6)
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            image_template = cv2.imread(self.systemlogin_icon)
            result = cv2.matchTemplate(screenshot, image_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            image_height, image_width, _ = image_template.shape
            center_x = max_loc[0] + image_width // 2
            center_y = max_loc[1] + image_height // 2
            pyautogui.moveTo(center_x, center_y)
            pyautogui.doubleClick()
            safe_sleep(6)
            pyautogui.click(self.username_field_location)
            pyautogui.write(username)
            pyautogui.click(self.password_field_location)
            pyautogui.write(password)
            pyautogui.press("enter")
            safe_sleep(6)
        except Exception as e:
            print('login error:', e)

    def entry_QA32 (self):
        try:
            pyautogui.click(81 , 52 )
            pyautogui.write("QA32")
            pyautogui.press("enter")
            safe_sleep(5)
        except:
            print('login error')

    def information_intlot (self,plant,inptype):
        try:
            # Lot Created On
            pyautogui.click(395 , 203 )
            pyautogui.hotkey("ctrl","a")
            pyautogui.press("backspace")
            current_date = datetime.now() # Format the date as "xx.xx.xxxx" 
            start_date = current_date - timedelta(days=15)
            start_date = start_date.strftime("%d.%m.%Y")
            pyautogui.write(start_date)
            
            # Plant
            pyautogui.click(339 , 270 )
            pyautogui.write(plant)
            pyautogui.click(304 , 262 ) #Clear popup Plant

            #Insp. Lot Origin
            pyautogui.click(333 , 292 )
            pyautogui.write(inptype)
            pyautogui.click(304 , 262 )

            #select only with out inspection UD
            pyautogui.click(45 , 538 )

            #choose Layout
            pyautogui.click(430 , 579 )
            pyautogui.hotkey("ctrl","a")
            pyautogui.press("backspace")
            pyautogui.write("/ALL-QMBOT")

            #Execute
            pyautogui.hotkey("Fn","F8" )
            safe_sleep(10)
        except:
            print('information_intlot error')

    def filt_multi_status(self) : # Filter short text Reject
        try:
           
            pyautogui.click(433, 159)
            pyautogui.hotkey("shift","f4")
            safe_sleep(3)
            pyautogui.click(1273,753)
            safe_sleep(3)
            pyautogui.write("INSP*")
            safe_sleep(3)
            pyautogui.press("enter")
            
        except:
            print('filt_multi_status error')
            
    def check_statusud(self):
        pyautogui.click(388,318)
        safe_sleep(5)
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        image_template = cv2.imread(self.statusud_icon)

        result = cv2.matchTemplate(screenshot, image_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # ถ้ามีความแม่นยำมากกว่า 0.10 (สามารถปรับตัวเลขนี้ได้ตามความต้องการ)
        if max_val > 0.8:
            image_height, image_width, _ = image_template.shape
            center_x = max_loc[0] + image_width // 2
            center_y = max_loc[1] + image_height // 2
            safe_sleep(5)
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click(188,314)
        else:
            # ถ้าไม่พบภาพ template ใน screenshot, คลิกที่ตำแหน่งอื่น
            pyautogui.hotkey("F3")
            return False
        return True
   
    def ud_Char (self):
        try:
                pyautogui.click(205 , 909 )
                safe_sleep(5)
                pyautogui.write("A")
                safe_sleep(5)
                pyautogui.press("enter")
                safe_sleep(3)
                pyautogui.click(364,371 ) 
                safe_sleep(3)
                pyautogui.hotkey('ctrl','s')
                safe_sleep(5)
   
        except Exception as e:
            print('ud_Char error:', e)

    def check_popup(self):   
        
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        image_template = cv2.imread(self.chagelongtextud_icon)

        result = cv2.matchTemplate(screenshot, image_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # ถ้ามีความแม่นยำมากกว่า 0.5 (สามารถปรับตัวเลขนี้ได้ตามความต้องการ)
        if max_val > 0.7:
            safe_sleep(3)
            pyautogui.click(267,51)
            return True
        else:
        # ถ้าไม่พบภาพ template ใน screenshot, หยุดการทำงานของ function
            return False
        
        # Function สำหรับ วน loop ขยับแถวลง แล้วทำงาน ตาม Fucntion
    def process_rows(self, reference_position=(69,178), num_rows=4, col_widths=[50, 120, 122]):
        self.filt_multi_status()
        row_height = 20  # ระยะระหว่างแถวใน pixel

        for i in range(num_rows):
            self.select_ud_row(reference_position, 1, col_widths)  # เลือกแถวที่ i
            self.ud_step()  # ทำขั้นตอนการอัปเดต

            # อัปเดตตำแหน่งอ้างอิงสำหรับแถวถัดไป
            reference_position = (reference_position[0], reference_position[1] + row_height)

        return True

        # Function สำหรับ วน loop เลื่อนเก็บ Copy text inslot,Material ,batch ,ud code
    def select_ud_row(self ,reference_position, num_rows, col_widths):
        for i in range(num_rows):
            for j in range(3):
                new_position = (reference_position[0] + sum(col_widths[:j+1]), reference_position[1])
                pyautogui.moveTo(new_position, duration=1)
                pyautogui.click(new_position, button='right')
                safe_sleep(1)
                pyautogui.click((new_position[0]+10, new_position[1]+10), button='left')
                safe_sleep(1)
                if j == 0:
                    inslot = pyperclip.paste()
                elif j == 1:
                    material = pyperclip.paste()
                elif j == 2:
                    batch = pyperclip.paste()
                    udcode = "A"
                    safe_sleep(10)

        pyautogui.hotkey("ctrl","shift","f5")
        safe_sleep(3)
        return inslot, material, batch,udcode
    
    # Function สำหรับ UD check_statusud >> ud_Char >>check_popup
    def ud_step(self,plant_code):
        bot_start = datetime.now() 
        try:
            status_check = self.check_statusud()
            if not status_check:
                print("check_statusud returned False. Stopping ud_step.")
                return
            time.sleep(3)

            self.ud_Char()
            time.sleep(3)
            bot_end = datetime.now()

            # get data from select_ud_row
            inslot, material, batch, udcode = self.select_ud_row((69,178), 4, [50, 120, 122])

            # Save data to the database using save_bot_data
            self.udbot_data.save_bot_data(bot_start, bot_end, plant_code, material, batch, inslot, udcode)

            self.check_popup()
            time.sleep(3)
        except:
            print('ud_step error')
     
    def close_connection(self):
        try:
            pyautogui.click(791,20)
            safe_sleep(1)
            pyautogui.hotkey("alt","F4")
            safe_sleep(3)
            pyautogui.hotkey("ctrl","left")
            safe_sleep(3)
            pyautogui.press("enter")
        except:
            print('close_connection error') 

            




