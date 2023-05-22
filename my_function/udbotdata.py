from datetime import datetime
from mydb.db import Database
from smtplib import SMTP
from email.mime.text import MIMEText
from linebot import LineBotApi
from linebot.models import TextSendMessage
import configparser
from mydb.db import Database

# db = Database()

class UDBotData:
    def __init__(self):
        self.db = Database()

    def save_bot_data(self, bot_start, bot_end, plant, material, batch, inslot, udcode):
        bot_start_str = bot_start.strftime("%Y-%m-%d %H:%M:%S")
        bot_end_str = bot_end.strftime("%Y-%m-%d %H:%M:%S")

        # Insert data to the corresponding plant table
        self.db.insert_data(f'ubot_{plant}','bot_start, bot_end, plant, material, batch, inslot, udcode',[bot_start_str, bot_end_str, plant, material, batch, inslot, udcode])

    def get_and_send_data(self,plant):
        try:
            # Define the table and conditions for the select_data function
            table = f'ubot_{plant}'  # replace with your table name
            bot_start = datetime.datetime.now() - datetime.timedelta(hours=)
            bot_start = bot_start.strftime("%Y-%m-%d %H:00:00")
            bot_end = datetime.datetime.now()
            bot_end = bot_end.strftime("%Y-%m-%d %H:00:00")
            conditions = {
                "bot_start": bot_start
            }
            # Call the select_data function
            data_rows = self.db.select_data(table, conditions)

            # Count the number of rows returned by the select_data function
            inslot_count = len(data_rows)

            return plant, inslot_count, bot_start, bot_end

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