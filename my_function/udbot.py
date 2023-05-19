import pyautogui
import pyperclip
import time
from datetime import datetime, timedelta

def safe_sleep(duration):
    '''A wrapper function for time.sleep()'''
    time.sleep(duration)

class SAPLoginBot:
    
    def __init__(self):
        # Setting initial screen positions for SAP icon, login fields, etc.
        self.sap_icon_location = (53, 629)
        self.systemlogin= (288,478)
        self.username_field_location = (229, 206)
        self.password_field_location = (214, 230)
        self.login_button_location = (600, 600)

    def login(self, username, password):
        try:
            pyautogui.doubleClick(self.sap_icon_location)
            safe_sleep(10)
            pyautogui.doubleClick(self.systemlogin)
            safe_sleep(10)
            pyautogui.doubleClick(self.username_field_location)
            safe_sleep(5)
            pyautogui.click(self.username_field_location)
            pyautogui.write(username)
            pyautogui.click(self.password_field_location)
            pyautogui.write(password)
            pyautogui.press("enter")
            safe_sleep(10)
        except Exception as e:
            print('login error:', e)

    def entry_QA32 (self):
        try:
            pyautogui.click(81 , 52 )
            pyautogui.write("QA32")
            pyautogui.press("enter")
            time.sleep(10)
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
            pyautogui.write("/ALL-QM")

            #Execute
            pyautogui.hotkey("Fn","F8" )
            time.sleep(10)
        except:
            print('information_intlot error')

    def filt_multi_status(self) : # Filter short text Reject
        try:
            pyautogui.hotkey("shift","f2")
            pyautogui.keyDown('ctrl')
            pyautogui.click(989 , 157 )
            time.sleep(3)
            pyautogui.click(1353, 157 )
            pyautogui.keyUp('ctrl')
            pyautogui.hotkey("shift","f4")
            time.sleep(3)
            pyautogui.click(1273,753)
            pyautogui.write("INSP*")
            time.sleep(3)

            pyautogui.click(726,255)
            time.sleep(3)
            pyautogui.click(356,210)
            time.sleep(3)
            pyautogui.write("R*")
            pyautogui.hotkey("f8")
            time.sleep(3)
            pyautogui.press("enter")
        except:
            print('filt_multi_status error')  
  
    def change_intlot_data (self):
        try:
            #Filter system status
            self.filt_multi_status()
            time.sleep(3)

            #UD Inspectio lot
            pyautogui.hotkey("ctrl","shift","f5")
            time.sleep(3)
        except:
            print('change_intlot_data error')  
    
    def ud_Char (self):
        try:
            pyautogui.click(178 , 317 )
            pyautogui.click(205 , 909 )
            safe_sleep(5)
            pyautogui.write("A")
            safe_sleep(5)
            pyautogui.press("enter")
            safe_sleep(3)
            pyautogui.click(364,371 ) 
            safe_sleep(3)
            pyautogui.hotkey('ctrl','s')
            safe_sleep(3)
        except Exception as e:
            print('ud_Char error:', e)  

    def close_connection(self):
        try:
            pyautogui.click(791,20)
            time.sleep(1)
            pyautogui.hotkey("alt","F4")
            time.sleep(3)
            pyautogui.hotkey("ctrl","left")
            time.sleep(3)
            pyautogui.press("enter")
        except:
            print('close_connection error') 

