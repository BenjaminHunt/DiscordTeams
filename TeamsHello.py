# Work with Python 3.6
import sys
import discord
from discord.ext import commands
from Season import Match
from Team import Team

TOKEN = sys.argv[1]
print(TOKEN)

client = discord.Client()
teams = []
games = []

BOT_PREFIX = ('?', '!')
bot = commands.Bot(command_prefix=BOT_PREFIX, description="Teams & Leagues Bot!")

@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command(brief="Repeats your message", pass_context=True)
async def hello(context):
    await bot.say('Hello ' + context.message.author.mention)

@bot.command(pass_context=True)
async def repeat(ctx):
    await bot.say(ctx.message.content)

@bot.command(pass_context=True, brief="Creates a new team with 0..n players")
async def newteam(context):
    array = message_to_args(context.message.content)
    team = array[0]
    members = array[1:]

    team = Team(name=team, members=members)
    msg = ('New Team Created!\n' + team.to_s())
    await client.send_message(context.message.channel, msg)

'''
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    array = message.content.split(",")
    if len(array) > 1:
        cmd = array[0][:array[0].find(' ')]
        firstparam = array[0][array[0].find(' '):].strip()
        array = [firstparam] + array[1:]
    else:
        cmd = array[0]

    i = 0
    while i < len(array):
        array[i] = array[i].strip()
        i += 1

    print(cmd)
    print(array)

    #!newteam <team name>, member1, member2, ..., membern
    if cmd == "!newteam":
        team = array[0]
        members = array[1:]

        team = Team(name=team, members=members)
        msg = ('New Team Created!\n' + team.to_s()).format(message)
        await client.send_message(message.channel, msg)
        #teams += [team]

    #!newmatch <team1>, <team2>, <mon d yyyy hh:mm(AM/PM)>, <location>
    elif cmd == "!newmatch":
        match = Match(array[0], array[1], array[2], array[3])
        msg = 'New Match Created!\n' + match.to_s()
        await client.send_message(message.channel, msg)

'''
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def message_to_args(message):
    array = message.content.split(",")
    if len(array) > 1:
        firstparam = array[0][array[0].find(' '):].strip()
        array = [firstparam] + array[1:]

    i = 0
    while i < len(array):
        array[i] = array[i].strip()
        i += 1

    return array

bot.run(TOKEN)