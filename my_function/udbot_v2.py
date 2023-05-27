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

        project_dir = os.getcwd()  # หรือกำหนดเส้นทางของโปรเจคโดยตรง
        picture_dir = os.path.join(project_dir, 'documents', 'pictures')  # creates the path to the 'pictures' folder

        self.sap_icon_logo = os.path.join(picture_dir, 'saplogo.png')
        self.systemlogin_icon = os.path.join(picture_dir, 'Systemlogin.png')
        self.statusud_icon = os.path.join(picture_dir, 'StatusUD.png')
        self.changelongtextud_icon = os.path.join(picture_dir, 'changelongtextUD1.png')
        

        self.username_field_location = (218, 205)
        self.password_field_location = (205, 228)
        self.reference_position = (28, 182)
        
        # self.login_button_location = (600, 600)

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
            safe_sleep(5)
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
            safe_sleep(7)
            pyautogui.click(self.username_field_location,duration=1)
            pyautogui.write(username)
            safe_sleep(1)
            pyautogui.click(220, 205)
            safe_sleep(1)
            pyautogui.click(self.password_field_location,duration=1)
            pyautogui.write(password)
            pyautogui.press("enter")
            safe_sleep(7)
        except Exception as e:
            print('login error:', e)

    def entry_QA32 (self):
        try:
            pyautogui.click(81 , 52 )
            pyautogui.write("QA32")
            pyautogui.press("enter")
            safe_sleep(3)
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
            safe_sleep(5)
        except:
            print('information_intlot error')

    def filt_multi_status(self) : # Filter short text Reject
        try:
           
            pyautogui.click(433, 159)
            pyautogui.hotkey("shift","f4")
            safe_sleep(3)
            pyautogui.write("INSP*")
            safe_sleep(3)
            pyautogui.press("enter")
            
        except:
            print('filt_multi_status error')
     
    def ud_Char (self):
        try:
                pyautogui.click(203,885)
                safe_sleep(3)
                pyautogui.write("A")
                safe_sleep(3)
                pyautogui.press("enter")
                safe_sleep(3)
                pyautogui.click(364,371 ) 
                safe_sleep(3)
                pyautogui.hotkey('ctrl','s')
                safe_sleep(3)
   
        except Exception as e:
            print('ud_Char error:', e)     
            
            
    def check_popup(self):   
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        image_template = cv2.imread(self.changelongtextud_icon)

        result = cv2.matchTemplate(screenshot, image_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # If the accuracy is higher than 0.8 
        if max_val > 0.8:
            safe_sleep(5)
            pyautogui.click(267, 53, duration=1)
            return True
        else:
            # If the template image is not found in the screenshot, stop the function
            return False
        
    # Function สำหรับ วน loop ขยับแถวลง แล้วทำงาน ตาม Fucntion            
    def check_statusud(self,plant_code):
        pyautogui.click(388,318)
        safe_sleep(3)
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
            safe_sleep(6)
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click(188,314)
            self.ud_Char()
            self.check_popup()     
        else:
            # ถ้าไม่พบภาพ template ใน screenshot, คลิกที่ตำแหน่งอื่น
            pyautogui.hotkey("F3")
            return False
        return True
    
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
                    safe_sleep(5)

        pyautogui.hotkey("ctrl","shift","f5")
        safe_sleep(3)
        return inslot, material, batch,udcode
      
    def process_rows(self,plant_code, num_rows, col_widths=[70, 120, 122]):
        bot_start = datetime.now() 
        self.filt_multi_status()
        row_height = 20  # pixel distance between rows

        for i in range(num_rows):
            inslot, material, batch, udcode = self.select_ud_row(self.reference_position, 1, col_widths)  # select row i
            safe_sleep(3)
            self.check_statusud(plant_code)  # Check the status
          

            # update reference position for next row
            self.reference_position = (self.reference_position[0], self.reference_position[1] + row_height)
            bot_end = datetime.now()
            self.udbot_data.save_bot_data(bot_start, bot_end, plant_code, material, batch, inslot, udcode)

        return True
   
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

            




