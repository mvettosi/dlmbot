#!/usr/bin/env python3.7

from discord.ext.commands import Bot
from discord.ext import commands
from discord.enums import ChannelType
from dlmbot import persistence
import pprint

client = Bot(command_prefix='!')


# Startup
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# Message listener
@client.event
async def on_message(message):
    # Ignore messages from ourselves
    if message.author == client.user:
        return

    await remind_submission(message)
    await client.process_commands(message)


# Bot Commands
@client.command(pass_context=True)
async def setreminders(context, frequency=persistence.DEFAUT_FREQUENCY):
    # Optimally we would use commands.check decorator, but it fails without explaining why
    if is_dm(context):
        persistence.set_frequency(context.message.author.id, frequency)


@client.command(pass_context=True)
async def noremainders(context):
    # Optimally we would use commands.check decorator, but it fails without explaining why
    if is_dm(context):
        persistence.set_frequency(context.message.author.id, persistence.DEFAUT_FREQUENCY * 365)


# Functions
def run_bot():
    client.run('NTU4NTczNzkxODc4MzE2MDMz.D3Y0eA.spp5cP99uc5J_3F56ZCVBnFR1Pk')


def is_dm(context):
    return context.message.channel.type == ChannelType.private


def is_image(text):
    extensionsToCheck = ['.jpg', '.png', '.jpeg']
    return any(text.endswith(ext) for ext in extensionsToCheck)


def contains_image(message):
    return is_image(message.content) or any(is_image(attachment['filename']) for attachment in message.attachments)


async def remind_submission(message):
    # Ignore non-kog-decks channels
    if not message.channel.name or message.channel.name.startswith('kog-decks-'): return
    # Ignore messages that does not contain a deck
    if not contains_image(message): return
    # Skip if the user should not be reminded
    author = message.author
    if not persistence.should_be_reminded(author.id): return

    remind_message = '''
Hey there! I noticed you just uploaded an image in a kog-decks channel.
Good job!
Why don't you go even further and post it on DLM offical website, too?
Now you can do it by yourself!
Just follow these instructions:
    1) Go to https://www.duellinksmeta.com/top-decks/submit-your-deck/
    2) Login using discord
    3) Fill the form
    4) Push the submit button
    5) Done!

If you don't want to receive this reminder anymore, just use the
`!noreminders` command.
    '''
    await client.send_message(author, remind_message)

    persistence.reminded(author.id)
