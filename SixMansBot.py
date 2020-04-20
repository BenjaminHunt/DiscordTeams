# bot.py

import asyncio
from discord.ext import commands
import random
import sys

global games
games = []


class SixManGame:
    def __init__(self, home, away):
        self.home_team = home
        self.away_team = away

    async def teardown(self):
        await self.home_team.teardown()
        await self.away_team.teardown()

    def has_player(self, player):
        return player in self.home_team.get_players() or player in self.away_team.get_players()


class SixManTeam:
    def __init__(self, waiting_room, voice_channel, players=[]):
        self.waiting_room = waiting_room
        self.voice_channel = voice_channel
        self.players = players

    async def add_player(self, player):
        self.players.append(player)
        await player.move_to(self.voice_channel)

    def get_players(self):
        return self.players

    async def teardown(self):
        for player in self.players:
            await player.move_to(self.waiting_room)
        await self.voice_channel.delete(reason="6-Mans Teardown")


def run():
    token = sys.argv[1]
    print("Token: " + token)

    bot_prefix = ('?', '!')
    bot = commands.Bot(command_prefix=bot_prefix, description="Teams & Leagues Bot!")

    # These would be set per channel, not sure how RSC would implement:
    six_man_cat_id = 701497470101749850
    bot_input = 512343431213875203
    waiting_room_voice_id = 701497581942865961

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

        if len(player_pool) <= 0:
            return None

        six_mans_category = bot.get_channel(six_man_cat_id)
        waiting_room = bot.get_channel(waiting_room_voice_id)
        home_voice = await six_mans_category.create_voice_channel(name="Orange Team")
        away_voice = await six_mans_category.create_voice_channel(name="Blue Team")

        home_team = SixManTeam(waiting_room, home_voice)
        away_team = SixManTeam(waiting_room, away_voice)

        global games
        games.append(SixManGame(home=home_team, away=away_team))

        num_players = len(player_pool) if len(player_pool) < 6 else 6
        for i in range(0, num_players):
            player_pool = bot.get_channel(waiting_room_voice_id).members
            player = random.choice(player_pool)
            team = [home_team, away_team][i % 2]
            await team.add_player(player)

    @bot.command(name="game_over", aliases=["gameover", "gg", "ggs", "done"], brief="Regroup Teams",
                 help="Moves all 6-man players back into the waiting room", pass_context=True)
    async def game_over(context):
        player = context.message.author
        for game in games:
            if game.has_player(player):
                await game.teardown()

    bot.run(token)


run()
