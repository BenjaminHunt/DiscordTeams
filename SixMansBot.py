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

    async def remove_player(self, player):
        if player in self.home_team.get_players():
            await self.home_team.remove_player(player)
        elif player in self.away_team.get_players():
            await self.away_team.remove_player(player)

        # time.sleep(3)
        if self.home_team.has_empty_voice() and self.away_team.has_empty_voice():
            await self.teardown()
            return False
        return True

    def has_player(self, player):
        return player in self.home_team.get_players() or player in self.away_team.get_players()

    async def create_teams(self, waiting_room, player_pool):
        num_players = len(player_pool) if len(player_pool) < 6 else 6
        for i in range(0, num_players):
            player_pool = waiting_room.members
            player = random.choice(player_pool)
            team = [self.home_team, self.away_team][i % 2]
            await team.add_player(player)


class SixManTeam:
    def __init__(self, waiting_room, voice_channel, players=[]):
        self.waiting_room = waiting_room
        self.voice_channel = voice_channel

    async def remove_player(self, player):
        if player in self.voice_channel.members:
            await player.move_to(None)

    async def add_player(self, player):
        await player.move_to(self.voice_channel)

    def get_voice(self):
        return self.voice_channel

    def get_players(self):
        return self.voice_channel.members

    def has_empty_voice(self):
        return len(self.voice_channel.members) == 0

    async def teardown(self):
        for player in self.voice_channel.members:
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
        home_voice = await six_mans_category.create_voice_channel(name="{}: Orange Team".format('1'))
        away_voice = await six_mans_category.create_voice_channel(name="{}: Blue Team".format('1'))

        home_team = SixManTeam(waiting_room, home_voice)
        away_team = SixManTeam(waiting_room, away_voice)

        global games
        game = SixManGame(home=home_team, away=away_team)
        await game.create_teams(waiting_room, player_pool)
        games.append(game)

    @bot.command(name="game_over", aliases=["gameover", "gg", "ggs", "done"], brief="Regroup Teams",
                 help="Moves all 6-man players back into the waiting room", pass_context=True)
    async def game_over(context):
        player = context.message.author
        for game in games:
            if game.has_player(player):
                await game.teardown()

    @bot.command(name="rms", aliases=["rmself", "removeself"], short="remove invoker", pass_context=True)
    async def rms(context):
        player = context.message.author
        for game in games:
            if game.has_player(player):
                game_continues = await game.remove_player(player)
                if not game_continues:
                    games.remove(game)

    @bot.command(name="clean", aliases=["cleanup", "smc", "sixmanclean", "6mc"],
                 short="delete all non-waiting room 6-man voice channels", pass_context=True)
    async def clean(context):
        six_mans_category = bot.get_channel(six_man_cat_id)
        waiting_room = bot.get_channel(waiting_room_voice_id)
        remove_channels = six_mans_category.channels
        remove_channels.remove(waiting_room)
        for channel in remove_channels:
            await channel.delete(reason="Cleanup")

    bot.run(token)


run()
