from datetime import datetime
from mydb.db import Database
from smtplib import SMTP
from email.mime.text import MIMEText
from linebot import LineBotApi
from linebot.models import TextSendMessage
import configparser
from mydb.db import Database
import datetime
# db = Database()

class UDBotData:
    def __init__(self):
        self.db = Database()
        self.db.connect()

    def save_bot_data(self, bot_start, bot_end, plant, material, batch, inslot, udcode):
        bot_start_str = bot_start.strftime("%Y-%m-%d %H:%M:%S")
        bot_end_str = bot_end.strftime("%Y-%m-%d %H:%M:%S")

        # Insert data to the corresponding plant table
        self.db.insert_data(f'ubot_{plant}','bot_start, bot_end, plant, material, batch, inslot, udcode',[bot_start_str, bot_end_str, plant, material, batch, inslot, udcode])

    def get_and_send_data_toline(self,plant):
        try:
            # Define the table and conditions for the select_data function
            table = f'ubot_{plant}'  # replace with your table name
            bot_start = datetime.datetime.now() - datetime.timedelta(hours=4)
            bot_start = bot_start.strftime("%Y-%m-%d %H:00:00")
            bot_end = datetime.datetime.now()
            bot_end = bot_end.strftime("%Y-%m-%d %H:00:00")
            conditions = {
                "bot_start": bot_start
            }
            data = self.db.select_data(table, conditions)
            inslot_count = data['inslot'].count()         
            return plant,inslot_count,bot_start,bot_end
            
        except Exception as e:
            print('Error:', e)
            
    def get_and_send_data_toemail(self,plant):
        try:
            # Define the table and conditions for the select_data function
            table = f'ubot_{plant}'  # replace with your table name
            bot_start = datetime.datetime.now() - datetime.timedelta(hours=24)
            bot_start = bot_start.strftime("%Y-%m-%d %H:00:00")
            bot_end = datetime.datetime.now()
            bot_end = bot_end.strftime("%Y-%m-%d %H:00:00")
            conditions = {
                "bot_start": bot_start
            }
            data = self.db.select_data(table, conditions)
            inslot_count = data['inslot'].count()         
            return plant,inslot_count,bot_start,bot_end
            
        except Exception as e:
            print('Error:', e)

    def send_email(self,plant,email):
        data = self.get_and_send_data_toemail(plant)
        plant = data[0]
        inslot_count = data[1]

        bot_start = data[2]
        bot_start = bot_start.split(' ')[1][:5]

        bot_end = data[3]
        bot_end = bot_end.split(' ')[1][:5]
        # Read line configuration from line_config.ini
        # Setup SMTP server and email properties
        smtp = SMTP("mail.mailserver.com")
        msg = MIMEText(f"{plant}, UD ins by udbot {inslot_count} ins.lots from since{bot_start}-{bot_end}")
        msg['Subject'] = 'UDBot Data Report'
        msg['From'] = 'mail@mail.com'
        msg['To'] = email

        # Send the email
        smtp.send_message(msg)
        smtp.quit()

    def send_line(self):
        data = self.get_and_send_data_toline(plant)
        plant = data[0]
        inslot_count = data[1]

        bot_start = data[2]
        bot_start = bot_start.split(' ')[1][:5]

        bot_end = data[3]
        bot_end = bot_end.split(' ')[1][:5]
        # Read line configuration from line_config.ini

        config = configparser.ConfigParser()
        config.read('config.ini')

        channel_access_token = config.get('line_config', 'ChannelAccessToken')

        # Setup Line bot API
        line_bot_api = LineBotApi(channel_access_token)

        # Send the Line message
        user_id = config.get('line_config', 'YouruserID')
        message = TextSendMessage(text=f"{plant}, UD ins by udbot {inslot_count} ins.lots from since{bot_start}-{bot_end}")
        line_bot_api.push_message(user_id, message)