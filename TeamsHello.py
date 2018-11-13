# Work with Python 3.6
import discord
from Season import Match
from Team import Team

TOKEN = 'NTExNjIwNjUwNDU3MjM1NDc3.DstnjA.c2um3wbDdGawmTxnDI9kE32h8ko'

client = discord.Client()
teams = []
games = []

@client.event
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

    #print(cmd)
    #print(array)

    #!hello
    if cmd == "!hello":
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    #!newteam <team name>, member1, member2, ..., membern
    elif cmd == "!newteam":
        team = array[0]
        members = array[1:]

        team = Team(name=team, members=members)
        msg = ('New Team Created!\n' + team.to_s()).format(message)
        await client.send_message(message.channel, msg)
        #teams += [team]

    #!newmatch <team1>, <team2>, <datetime>, <location>
    elif cmd == "!newmatch":
        match = Match(array[0], array[1], array[2], array[3])
        msg = 'New Match Created!\n' + match.to_s()
        await client.send_message(message.channel, msg)


    #other
    else:
        await client.send_message(message.channel, "Not a supported command.")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
