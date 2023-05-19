import pyautogui
import pyperclip
import time
from datetime import datetime, timedelta

class SAPLoginBot:
    def __init__(self):
        # Adjust these coordinates according to your screen resolution
        self.sap_icon_location = (53, 629)
        self.systemlogin= (531, 716)
        self.username_field_location = (229, 206)
        self.password_field_location = (214, 230)
        self.login_button_location = (600, 600)

    def login(self, username, password):
        # Double click on the SAP icon on the desktop
        pyautogui.doubleClick(self.sap_icon_location)
        time.sleep(10)  # Wait for the SAP login window to appear

        pyautogui.doubleClick(self.systemlogin)
        time.sleep(10)

        # Enter the username
        pyautogui.doubleClick(self.username_field_location)
        time.sleep(5)
        pyautogui.click(self.username_field_location)
        pyautogui.write(username)
    

        # Enter the password
        pyautogui.click(self.password_field_location)
        pyautogui.write(password)
        pyautogui.press("enter")
        time.sleep(10)


    def entry_QA32 (self):
        pyautogui.click(81 , 52 )
        pyautogui.write("QA32")
        pyautogui.press("enter")
        time.sleep(10)

    def information_intlot (self,plant):
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
        pyautogui.write("04")
        pyautogui.click(304 , 262 )

        #select only with out inspection UD
        pyautogui.click(45 , 538 )

        #choose Layout
        pyautogui.click(430 , 579 )
        pyautogui.hotkey("ctrl","a")
        pyautogui.press("backspace")
        pyautogui.write("/ALL-QM")

        #Execute
        pyautogui.hotkey("Fn","F8" )
        time.sleep(10)

    def change_intlot_data (self):
        #Filter system status
        pyautogui.click(989 , 157 )
        pyautogui.hotkey("shift","f4")
        time.sleep(3)
        pyautogui.write("INSP*")
        pyautogui.press("enter")
        time.sleep(3)

        #UD Inspectio lot
        pyautogui.hotkey("ctrl","shift","f5")

    
    def check_result (self): #Check Result form
        pyautogui.click(291 , 408 )
        pyautogui.hotkey("shift","left")
        pyautogui.hotkey("ctrl","c")
        ud_code = pyperclip.paste()
        return ud_code
    
    def ud_inform (self):
        ud_code = self.check_result()

    def close_connection(self):
        pass




    def bot_process(self,username, password ,plant):
        self.login(username, password)
        self.entry_QA32()
        self.information_intlot(plant)
        self.change_intlot_data()
        self.check_result()
        self.close_connection()

