# bot.py

import discord
from discord.ext import commands
import random

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
    waiting_room_voice_id = 701497581942865961
    home_voice_id = 701498135813423166
    away_voice_id = 701498234941603900

    @bot.event
    async def on_ready():
        print('{} logged in ({})'.format(bot.user.name, bot.user.id))
        print('------')

    @bot.command(name="start_six_mans",
                 aliases=["start", "startsixmans", "start6mans", "queue", "q", "6-mans"],
                 brief="Join 6-Man Queue",
                 help="Join 6-Man Queue. The Bot will take care of the rest.",
                 pass_context=True)
    async def start_six_mans(context):
        player_pool = bot.get_channel(waiting_room_voice_id).members

        if len(player_pool) < 6 and False:
            await context.send("Not enough players.")
        else:
            num_players = len(player_pool) if len(player_pool) < 6 else 6
            for i in range(0, num_players):
                player_pool = bot.get_channel(waiting_room_voice_id).members
                player = random.choice(player_pool)
                room = [home_voice_id, away_voice_id][i % 2]
                await player.move_to(bot.get_channel(room))

    @bot.command(name="game_over", aliases=["gameover", "gg", "ggs", "done"], brief="Regroup Teams",
                 help="Moves all 6-man players back into the waiting room", pass_context=True)
    async def game_over(context):
        for room in [away_voice_id, home_voice_id]:
            player_pool = bot.get_channel(room).members
            for player in player_pool:
                await player.move_to(bot.get_channel(waiting_room_voice_id))

    bot.run(token)


run()
