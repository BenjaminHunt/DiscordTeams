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
@bot.command(name="newteam",
             brief="Creates a new team with 0..n players",
             description="!newteam makes a new team with a set number of team players, and creates a new role for" +
                         " the team that can be mentioned (or called) to notify all team members." +
                         " Adding team players are optional, but highly encouraged." +
                         " Players may be added or removed from a team with the !addplayer or !removeplayer commands." +
                         " Team members must be part of the discord server." +
                         "\n\nFormat: !newteam <team name>, <member-1>, <member-2>, ..., <member-n>",
             pass_context=True)
async def new_team(context):
    server = get_server(context)
    array = message_to_array(context.message.content)
    team_name = array[0]

    role = await bot.create_role(server=server, name=team_name, hoist=True, mentionable=True)  # permissions, color
    valid_members, invalid_members = validate_members(server, array[1:])

    for member in valid_members:
       await bot.add_roles(server.get_member_named(member), role)  # add each valid member to team

    if len(invalid_members) != 0:
        invalid_response = get_invalid_members_response(invalid_members)
        await bot.say(invalid_response)

    team = Team(name=team_name, role=role, members=valid_members)  # members=members)
    msg = ('New Team Created!\n' + team.to_s())

    global teams
    teams = teams + [team]

    await bot.say(msg)


# !addplayers <team name>, <member1>, ..., <member n>
@bot.command(name="addplayers",
             aliases=["addplayer", "addtoteam"],
             brief="Adds one or more players to a pre-existing team.",
             description="!addplayers adds one to many players to a pre-existing team. For any action to be taken" +
                         " at least one player must be included." +
                         "\n\nFormat: !addplayers <team name>, <member-1>, <member-2>, ..., <member-n>",
             pass_context=True)
async def add_players(context):
    server = get_server(context)
    array = message_to_array(context.message.content)
    team_name = array[0]
    team = None

    #what is no additional parameters are passed? same for !newteam

    valid_members, invalid_members = validate_members(server, array[1:])

    global teams

    found = False
    for t in teams:
        if t.name == team_name:
            team = t
            found = True

    if not found:
        await bot.say("{} is not an existing team.".format(team_name))
        return

    for member in valid_members:
        team.add_member(member)
        await bot.add_roles(server.get_member_named(member), team.discord_role)  # add each valid member to team

    print(valid_members)
    print(invalid_members)
    if len(invalid_members) != 0:
        invalid_response = get_invalid_members_response(invalid_members)
        await bot.say(invalid_response)

    if len(valid_members) == 1:
        msg = (valid_members[0] + " was added to {}.".format(team_name))
    elif len(valid_members) > 1:
        msg = ', '.join(valid_members[:-1]) + " and " + valid_members[-1]
        msg += " were added to {}.".format(team_name)
    else:
        msg = "No members added to {}".format(team_name)
    await bot.say(msg)

    print(array)


@bot.command(name="roles",
             aliases=["teamroles"],
             brief="Create a new role, add user to it. This will be removed",
             pass_context=True)
async def show_roles(context):
    server = get_server(context)
    roles = server.roles  # ', '.join(server.roles)
    roles = roles[1:]
    await bot.say("Roles: {}".format(", ".join(map(str, roles))))


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


@bot.command(name="myteam",
             aliases=["whichteam"],
             brief="Lists your team if you're on one.",
             description="Lists the team the command caller is a member of." +
                         " The bot will also state if the invoker does not belong to a team.",
             pass_context=True)
async def my_team(context):
    member = str(context.message.author)
    global teams
    for team in teams:
        if member in team.members:
            await bot.say("Your team: {}".format(team.name))
            return
    await bot.say("You are not currently on a team.")


@bot.command(name="callben",
             aliases=["null", "callnull", "callnullidea"],
             brief="This mentions Ben (nullidea) from the bot.",
             description="This mentions Ben (nullidea from the Teams bot." +
                         " This was to test the server function, `get_member_named` function. +"
                         " Eventually, this command should be removed.",
             pass_context=True)
async def call_ben(context):
    server = get_server(context)  # Access server class
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
    first_param = array[0][array[0].find(' '):].strip()
    array = [first_param] + array[1:]
    i = 0
    while i < len(array):
        array[i] = array[i].strip()
        i += 1
    return array


def validate_members(server, all_members):
    valid = []
    invalid = []
    for member in all_members:
        if server.get_member_named(member) is not None:
            valid = valid + [member]
            # await bot.add_roles(server.get_member_named(member), team_role)  # for each member
        else:
            invalid += [member]
    return valid, invalid


def get_invalid_members_response(invalid_members):
    if len(invalid_members) == 1:
        invalid_response = (invalid_members[0] + " is not a valid discord member tag.")
    elif len(invalid_members) > 1:
        invalid_response = ', '.join(invalid_members[:-1]) + " and " + invalid_members[-1]
        invalid_response += " are not valid discord member tags."
    else:
        return "No invalid members. This line shouldn't be hit?"
    return invalid_response


def get_server(context):
    return context.message.author.server


bot.run(TOKEN)
