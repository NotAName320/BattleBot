import discord
from discord.ext import commands
import json
import random as r
from pretty_help import PrettyHelp, Navigation
from nation import Nation

# Sets help command options
nav = Navigation()
c = discord.Color.dark_orange()
# Requires members intent to search guild members list
intents = discord.Intents.default()
intents.members = True
# Sets bot variable to be accessed later.
help_command = PrettyHelp(navigation=nav, color=c, active_time=60)
client = commands.Bot(command_prefix='t!', intents=intents, help_command=help_command)
# Opens credentials.json and extracts bot token
credentials_file = open('credentials.json', 'r')
credentials = json.load(credentials_file)
credentials_file.close()
token = credentials['discord_token']


def checkRole(user, roleName):
    """Check if user is a specific role"""
    for role in user.roles:
        if role.name == roleName:
            return True
    return False


class Nations(commands.Cog, name='Nation Management'):
    def __init__(self, bot):
        self.bot = bot

    async def nation_to_embed(self, ctx, nation, message=''):
        """Sends nation info in an embed."""
        leader = self.bot.get_user(nation.leader)
        techs = '```'
        if len(nation.technology) == 0:
            techs += 'None'
        for x in range(len(nation.technology)):
            techs += f'{x}. {nation.technology[x].name}'
        techs += '```'
        embed = discord.Embed(title='Nation Info', color=nation.color)
        embed.add_field(name='Nation Name', value=nation.name, inline=True)
        embed.add_field(name='Nation Leader', value=leader.mention, inline=True)
        embed.add_field(name='Technologies Researched', value=techs, inline=False)
        await ctx.send(message, embed=embed)

    @commands.command(name='create-nation')
    async def createnation(self, ctx, *, name):
        """Creates a default nation which the user can then alter."""
        with open('nations.json') as f:
            data = json.load(f)
            if str(ctx.author.id) in data:
                await ctx.reply('You already have a nation. Please delete your nation first or edit it.')
                return
            else:
                nation = Nation(name=name, leader=ctx.author.id)
                data[str(ctx.author.id)] = nation.__dict__()
                await self.nation_to_embed(ctx, nation, 'Nation Created. t!edit-nation to edit.')
        f = open('nations.json', 'w')
        f.write(json.dumps(data, indent=4))
        f.close()


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll')
    async def roll(self, ctx, sides: int = 20):
        """Rolls a die with number of sides specified by the user."""
        random_number = r.randint(1, sides)
        await ctx.reply(f'The random number is {random_number}.')


def login():
    @client.event
    async def on_ready():
        # Prints login success and bot info to console
        print('Logged in as')
        print(client.user)
        print(client.user.id)
        # Sets bot activity for flair
        activity = discord.Activity(type=discord.ActivityType.watching, name='you all')
        await client.change_presence(activity=activity)

    # Adds cogs and runs bot
    client.add_cog(Miscellaneous(client))
    client.add_cog(Nations(client))
    client.run(token)
