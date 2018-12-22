# Work with Python 3.6
import sys
from discord.ext import commands
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


# !newteam <team name>, member1, member2, ..., membern
@bot.command(pass_context=True,
             brief="Creates a new team with 0..n players",
             description="!newteam makes a new team with a set number of team players." +
                         " Adding team players are optional, but highly encouraged." +
                         " Players may be added or removed from a team with the !addplayer or !removeplayer commands." +
                         " Team members must be part of the discord server." +
                         "\n\nFormat: !newteam <team name>, <member-1>, <member-2>, ..., <member-n>")
async def newteam(context):
    server = context.message.author.server
    array = message_to_array(context.message.content)
    teamname = array[0]
    members = []
    invalid = []

    for member in array[1:]:
        if server.get_member_named(member) is not None:  # check if valid member in the server
            members = members + [member]
        else:
            invalid += [member]

        invalid_response = ""
        if len(invalid) == 1:
            invalid_response = (invalid[0] + " is not a valid discord member tag.")
        elif len(invalid) > 1:
            invalid_response = ', '.join(invalid)
            invalid_response += " are not valid discord member tags."

    await bot.say(invalid_response)

    team = Team(name=teamname, members=members)  # members=members)
    msg = ('New Team Created!\n' + team.to_s())

    global teams
    teams = teams + [team]

    await bot.say(msg)


# !newmatch <team1>, <team2>, <mon d yyyy hh:mm(AM/PM)>, <location>
@bot.command(name="newmatch",
             aliases=["newgame"],
             brief="Schedule a new match.",
             description="!newmatch schedules a new match between two different teams." +
                         "\n\nFormat: !newmatch <team1>, <team2>, <mon d yyyy hh:mm(AM/PM)>, <location>",
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
             aliases=["null", "callnull", "callnullidea"],
             brief="This mentions Ben (nullidea) from the bot.",
             description="This mentions Ben (nullidea from the Teams bot." +
                         " This was to test the server function, `get_member_named` function. +"
                         " Eventually, this command should be removed.",
             pass_context=True)
async def call_ben(context):
    server = context.message.author.server  # Access server class
    await bot.say(server.get_member_named("nullidea#3117").mention)


@bot.command(name="printallmembers",
             aliases=["allmembers", "members", "thisserver"],
             brief="list and mention all members in server",
             description="Lists all members in a server. This command should eventually be removed.")
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
