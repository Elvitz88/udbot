# __udbot__
UDBot is an automation software designed to perform Robotic Process Automation (RPA) on a specific program. The bot is built in Python and is designed to perform tasks quickly and efficiently.

## __Setup Instructions__

Follow the steps below to set up and run UDBot:

### __Step 1: Clone the repository__
Clone the repository to your local machine.

    https://github.com/Elvitz88/udbot.git

### __Step 2: Create necessary directories__
Navigate to the root of the project and create the following directories:

    mkdir my_function
    mkdir mydb

These directories will store documents, custom function scripts, and databases, respectively.

### __Step 3: Create a virtual environment__
Create a Python virtual environment to isolate the project dependencies. You can do this by running the following command:

    python -m venv env

To activate the virtual environment, run:

    env\Scripts\activate.bat

### __Step 4: Install dependencies__
Install the necessary Python dependencies by running:

    pip install -r requirements.txt

This will install all the dependencies listed in the requirements.txt file.

## __Running the Bot__
After setting up, you can run UDBot by executing the main Python script (please replace main_script.py with the actual name of your script):

    python main_script.py

## __Contributing__
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## __License__
UDBot is licensed under the terms of the [MIT License.](https://choosealicense.com/licenses/mit/)