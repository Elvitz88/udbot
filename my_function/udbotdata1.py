import os
import pandas as pd

class UDBotData1:
    # ...

    def save_bot_data(self, bot_start, bot_end, plant, material, batch, inslot, udcode, user):
        bot_start_str = bot_start.strftime("%Y-%m-%d %H:%M:%S")
        bot_end_str = bot_end.strftime("%Y-%m-%d %H:%M:%S")

        data = {
            'bot_start': [bot_start_str],
            'bot_end': [bot_end_str],
            'plant': [plant],
            'material': [material],
            'batch': [batch],
            'inslot': [inslot],
            'udcode': [udcode],
            'user' : [user]
        }

        # Use plant to create a filename and check if the folder exists, if not create one
        date_str = bot_start.strftime("%Y-%m-%d")
        directory = f'documents/datalog/{plant}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f'{directory}/{date_str}.csv'

        df = pd.DataFrame(data)

        # Check if the file exists
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, mode='w', index=False)

    # ...




