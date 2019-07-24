#!/usr/bin/env python3.7

from discord.ext import commands
from discord.abc import PrivateChannel
from utils import persistence
import calendar
import re


class MordoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    # Message listener
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from ourselves
        if message.author == self.bot.user:
            return

        await remind_submission(message)

    # Bot Commands
    @commands.command(pass_context=True)
    async def remindon(self, context, frequency=persistence.DEFAUT_FREQUENCY):
        # Optimally we would use commands.check decorator, but it fails without explaining why
        if isinstance(context.message.channel, PrivateChannel):
            persistence.set_frequency(context.message.author.id, frequency)
            await context.message.author.send('Remainders activated')

    @commands.command(pass_context=True)
    async def remindoff(self, context):
        # Optimally we would use commands.check decorator, but it fails without explaining why
        if isinstance(context.message.channel, PrivateChannel):
            persistence.set_frequency(
                context.message.author.id, persistence.DEFAUT_FREQUENCY * 365)
            await context.message.author.send('Remainders deactivated')


# Functions
def is_image(text):
    extensionsToCheck = ['.jpg', '.png', '.jpeg']
    return any(text.endswith(ext) for ext in extensionsToCheck)


def contains_urls(string):
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_regex, string)
    return len(urls) > 0


def contains_image(message):
    return contains_urls(message.content) or any(is_image(attachment.filename) for attachment in message.attachments)


async def remind_submission(message):
    # Ignore non-kog-decks channels
    regex = f'^kog-decks-({"|".join([calendar.month_name[month_val].lower() for month_val in range(1, 13)])})'
    pattern = re.compile(regex)
    if isinstance(message.channel, PrivateChannel) or message.channel.name is None or not pattern.match(
            message.channel.name):
        print('Received message from a non-kog channel')
        return
    # Ignore messages that does not contain a deck
    if not contains_image(message):
        print('Received message not containing an image')
        return
    # Skip if the user should not be reminded
    author = message.author
    if not persistence.should_be_reminded(author.id):
        print(f'Author {author} should not be reminded at this time')
        return

    remind_message = '''
Hello, I am Mordo! :robot:

My robot senses are telling me that you just posted your King of Games deck in the Duel Links Meta discord.

Thank you for that, we greatly appreciate your effort! └[ ∵ ]┘

Did you know that you can also **submit your deck to the website**? This will make it appear in the top-decks section.

You can do so here: https://www.duellinksmeta.com/top-decks/submit-your-deck/.

Just fill in the form, add your cards, write up your notes and smash that submit button.
**Gif showing you how to Submit**: https://imgur.com/a/dMjQTmE

If you don't want me to remind you anymore, you can do so by using the command `!remindoff`, I'm a robot after all. You can activate me again with `!remindon`. Both commands will only work in our private conversation.

In case you didn't shut me down, see you next month! I'll be back. [┐∵]┘
    '''
    await author.send(remind_message)

    persistence.reminded(author.id)


def setup(bot):
    bot.add_cog(MordoCog(bot))
