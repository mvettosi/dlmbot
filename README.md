# dlmbot (Aka Mordo)

Discord bot written in python to provide functionalities to the Duel Links Meta discord server.
Currently, the bot includes the following features:
- Mordo, to remind users that submit decks in a kog-decks channel, to do so on the website as well

The bot uses discord.py and tinydb for the persistence.

## Run this bot
The bot requires python 3.6 installed on the system.
Follow these steps to run the bot on your own (Unix-based) machine.

### Create a test Bot Token
The bot will need a test token to run. To get one simply follow this guide: https://www.writebots.com/discord-bot-token/ (you can skip the part about getting an icon =P).

### Create a configuration file
Now that you have a token, copy-paste the `data/config.json.example` into a file named `data/config.json` and insert the token into the related field.

### Create a python venv (Virtual Environment) and install dependencies
Now you want to create an encapsulated environment to install the project dependencies without messing with the system or user scope of your python installation.
Do achieve this, use the following commands:
```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python ./bot.py
```
When you are done, to exit the virtual environment, just run the command
```
deactivate
```
