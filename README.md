# dlmbot (Aka Mordo)

Discord bot written in python to remind users that submit decks in a kog-decks channel, to do so on the website as well.

It uses discord.py v.1.0.0a and tinydb for the persistence.

## To run this bot
There are two ways to run this bot.

### Directly
Requires python 3.6 installed.
Follow these steps:
```bash
python -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py
python -m pip install -r requirements.txt
python -m pip install .
python -m dlmbot
```

### Docker
Requires docker installed locally.
Just run
```bash
./run.sh
```
