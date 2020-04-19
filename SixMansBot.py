# bot.py

import discord
from discord.ext import commands
from discord.ext.commands import Bot

import sys


class SixManTeam:
    def __init__(self, voice_channel, players=[]):
        self.voice_channel = voice_channel
        self.players = players


class SixMans:
    def __init__(self, players=[]):
        self.players = players
        self.home = []
        self.away = []


def run():
    token = sys.argv[1]
    print("Token: " + token)

    bot_prefix = ('?', '!')
    bot = commands.Bot(command_prefix=bot_prefix, description="Teams & Leagues Bot!")

    # These would be set per channel, not sure how RSC would implement:
    bot_input = 512343431213875203
    waiting_room = 701497581942865961
    home_voice_id = 701498135813423166
    away_voice_id = 701498234941603900

    @bot.event
    async def on_ready():
        print('{} logged in ({})'.format(bot.user.name, bot.user.id))
        print('------')

    @bot.command(name="queue", aliases=["q"], brief="Join 6-Man Queue", help="Join 6-Man Queue. The Bot will take care of the rest.", pass_context=True)
    async def queue(context):
        await context.message.channel.send("I see you.")
        player_pool = bot.get_channel(waiting_room).members
        for player in player_pool:
            await bot.move_members(player, home_voice_id)

    bot.run(token)


run()
