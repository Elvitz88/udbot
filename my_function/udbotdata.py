from datetime import datetime, timedelta
from mydb.db import Database
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class UDBotData:
    def __init__(self):
        self.db = Database()
        self.db.connect()

    def save_bot_data(self, bot_start, bot_end, plant, material, batch, inslot, udcode):
        bot_start_str = bot_start.strftime("%Y-%m-%d %H:%M:%S")
        bot_end_str = bot_end.strftime("%Y-%m-%d %H:%M:%S")

        # Insert data to the corresponding plant table
        self.db.insert_data(f'ubot_{plant}','bot_start, bot_end, plant, material, batch, inslot, udcode',[bot_start_str, bot_end_str, plant, material, batch, inslot, udcode])
        
    def get_and_send_data_toemail(self, plant):
        try:
            nows = datetime.datetime.now()
            bot_start = (nows - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')  # 1 day ago
            bot_end = nows.strftime('%Y-%m-%d %H:%M:%S')  # now
                        
            data = self.db.get_data(plant, bot_start, bot_end)
            inslot_count = data['inslot'].count()
            return data,plant, bot_start,bot_end,inslot_count

        except Exception as e:
            print('Error:', e)
        
    def send_email(self,from_email,plant, to_email, mail_server, username, password):
        # Create the body of the email
        datas = self.get_and_send_data_toemail(plant)
        data = datas[0]
        plant = datas[1]
        bot_start = datas[2]
        bot_end = datas[3]
        inslot_count = datas[4]
        subject = 'สรุปผลการทำงานของ Usage Decision by UDBOT'

        message = f'UD_Bot process {plant} from {bot_start} to {bot_end}:'
        message += f'Total inspection Lot: {inslot_count}'
        # message += f'Data:\n{data.to_string()}'

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.office365.com', 587)  # Office 365 server
            server.ehlo()  # optional, called by login()
            server.starttls()  # required for starttls
            server.login(username, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.close()

            print('Email sent!')

        except Exception as e:
            print('Something went wrong...', e)