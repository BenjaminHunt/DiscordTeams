# Work with Python 3.6
import sys
from discord.ext import commands
from discord import Server
from Season import Match
from Team import Team

global teams, games, people
teams = []
games = []
people = []

TOKEN = sys.argv[1]
print("Token: " + TOKEN)

BOT_PREFIX = ('?', '!')
bot = commands.Bot(command_prefix=BOT_PREFIX, description="Teams & Leagues Bot!")


# ############################################# COMMANDS ##############################################

@bot.command(brief="Repeats your message", pass_context=True)
async def hello(context):
    await bot.say('Hello ' + context.message.author.mention)


@bot.command(brief="test random things")
async def test():
    await bot.say("<@302079469882179585>" + " --called out.")


@bot.command(pass_context=True)
async def repeat(ctx):
    await bot.say(ctx.message.content)


# !newteam <team name>, member1, member2, ..., membern
@bot.command(pass_context=True, brief="Creates a new team with 0..n players")
async def new_team(context):
    array = message_to_array(context.message.content)
    team = array[0]
    members = array[1:]

    team = Team(name=team, members=members)
    msg = ('New Team Created!\n' + team.to_s())

    global teams
    teams = teams + [team]

    await bot.say(msg)


# !newmatch <team1>, <team2>, <mon d yyyy hh:mm(AM/PM)>, <location>
@bot.command(name="newmatch",
             aliases=["newgame"],
             brief="Schedule a new match.",
             pass_context=True)
async def new_match(context):
    array = message_to_array(context.message.content)
    match = Match(1, array[0], array[1], array[2], array[3])  # generate id for reporting score
    msg = 'New Match Created!\n' + match.to_s()
    global games
    games = games = [match]
    await bot.say(msg)


@bot.command(name="listteams",
             aliases=["allteams", "showteams", "teams"],
             brief="lists all teams in the league",
             pass_context=False)
async def list_teams():
    global teams
    if len(teams) == 0:
        await bot.say("There are no teams in this league!")
    else:
        str = "Teams: \n"
        for team in teams:
            str += team.name + ", "
        str = str.rstrip(", ")
        await bot.say(str)


@bot.command(name="callben",
             pass_context=True,
             brief="@ben")
async def call_ben(context):
    server = context.message.author.server  # Access server class
    await bot.say(server.get_member_named("nullidea#3117").mention)


@bot.command(name="printallmembers",
             brief="list and mention all members in server")
async def print_all_members():
    members = bot.get_all_members()
    for member in members:
        await bot.say(member)  # member.mention mentions member (@)
        global people
        people += [member]


# ####################################################################################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def message_to_array(message):
    array = message.split(",")
    if len(array) > 1:
        firstparam = array[0][array[0].find(' '):].strip()
        array = [firstparam] + array[1:]
    i = 0
    while i < len(array):
        array[i] = array[i].strip()
        i += 1
    return array

bot.run(TOKEN)
