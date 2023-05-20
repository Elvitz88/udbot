from datetime import datetime
from mydb.db import Database
from smtplib import SMTP
from email.mime.text import MIMEText
from linebot import LineBotApi
from linebot.models import TextSendMessage

class UDBotData:
    def __init__(self):
        self.db = Database()

    def save_bot_data(self, bot_start, bot_end, plant, material, batch, inslot, udcode):
        # Convert bot_start and bot_end to string in the appropriate format
        bot_start_str = bot_start.strftime("%Y-%m-%d %H:%M:%S")
        bot_end_str = bot_end.strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert data to the corresponding plant table
        self.db.insert_data(f'ubot_{plant}', 'bot_start, bot_end, plant, material, batch, inslot, udcode',
                            bot_start_str, bot_end_str, plant, material, batch, inslot, udcode)

    def get_and_send_data(self, plant):
        self.db.connect()
        data = self.db.select_data(f'ubot_{plant}', bot_start='2023-01-01 00:00:00', bot_end='2023-02-01 00:00:00', plant=plant)
        count_of_inslot = len([row for row in data if row['inslot'] == 'I1'])
        count_of_botstart = len([row for row in data if row['bot_start'] is not None])
        self.db.close_conn()

        self.send_email(plant, count_of_inslot, count_of_botstart)
        self.send_line_message(plant, count_of_inslot, count_of_botstart)

    def send_email(self, plant, count_of_inslot, count_of_botstart):
        # Setup SMTP server and email properties
        smtp = SMTP("smtp.mailserver.com")
        msg = MIMEText(f"For plant {plant}, there were {count_of_inslot} inslots and {count_of_botstart} bot starts.")
        msg['Subject'] = 'UDBot Data Report'
        msg['From'] = 'udbot@mail.com'
        msg['To'] = 'recipient@mail.com'

        # Send the email
        smtp.send_message(msg)
        smtp.quit()

    def send_line_message(self, plant, count_of_inslot, count_of_botstart):
        # Setup Line bot API
        line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')

        # Send the Line message
        line_bot_api.push_message('YOUR_USER_ID', TextSendMessage(
            text=f"For plant {plant}, there were {count_of_inslot} inslots and {count_of_botstart} bot starts."))