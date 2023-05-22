from datetime import datetime
from mydb.db import Database
from smtplib import SMTP
from email.mime.text import MIMEText
from linebot import LineBotApi
from linebot.models import TextSendMessage
import configparser
from mydb.db import Database

class UDBotData:
    def __init__(self):
        # Read configuration file
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Get PostgreSQL credentials
        host = config.get('postgresql', 'host')
        database = config.get('postgresql', 'database')
        user = config.get('postgresql', 'user')
        password = config.get('postgresql', 'password')
        port = config.get('postgresql', 'port')
        
        # Perform the database connection using the credentials
        self.db = Database(host, user, password, database, port)
        

    def save_bot_data(self, bot_start, bot_end, plant, material, batch, inslot, udcode):
        # Convert bot_start and bot_end to string in the appropriate format
        bot_start_str = bot_start.strftime("%Y-%m-%d %H:%M:%S")
        bot_end_str = bot_end.strftime("%Y-%m-%d %H:%M:%S")

        # Insert data to the corresponding plant table
        self.db.insert_data(f'ubot_{plant}', 'bot_start, bot_end, plant, material, batch, inslot, udcode',
                            bot_start_str, bot_end_str, plant, material, batch, inslot, udcode)

    def get_and_send_data(self, type, plant, email=None):
        try:
            data = self.db.select_data(plant)

            count_of_inslot = self.db.count_inslot(plant)
            count_of_botstart = self.db.count_botstart(plant)

            if type == 'email':
                self.send_email(email, data, count_of_inslot, count_of_botstart, plant)
            elif type == 'line':
                self.send_line(data, count_of_inslot, count_of_botstart, plant)

        except Exception as e:
            print('Error:', e)

    def send_email(self, email, data, count_of_inslot, count_of_botstart, plant):
        # Setup SMTP server and email properties
        smtp = SMTP("smtp.mailserver.com")
        msg = MIMEText(f"For plant {plant}, there were {count_of_inslot} inslots and {count_of_botstart} bot starts.")
        msg['Subject'] = 'UDBot Data Report'
        msg['From'] = 'udbot@mail.com'
        msg['To'] = email

        # Send the email
        smtp.send_message(msg)
        smtp.quit()

    def send_line(self, data, count_of_inslot, count_of_botstart, plant):
        # Read line configuration from line_config.ini
        config = configparser.ConfigParser()
        config.read('line_config.ini')

        channel_access_token = config.get('line_config', 'ChannelAccessToken')

        # Setup Line bot API
        line_bot_api = LineBotApi(channel_access_token)

        # Send the Line message
        user_id = config.get('line_config', 'YouruserID')
        message = TextSendMessage(text=f"For plant {plant}, there were {count_of_inslot} inslots and {count_of_botstart} bot starts.")
        line_bot_api.push_message(user_id, message)