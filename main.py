import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
load_dotenv(override=True)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TEST_CHANNEL = 986537383250001940
TEST_SERVER = discord.Object(id=969399636995493899)

# AUTH

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

# TODO: create list of who hasn't voted in specific vote
# TODO: create list of who voted for what
# TODO: multiple votes at once
# IDEA: nomination entity, list of votes/voters/comments, nominee name, comments bool?
# TODO: reminder to vote ping command
# TODO: reminder to vote DM command
# IDEA: easy to use!!! help command, good descriptions

# CODE

@discord.app_commands.guilds(TEST_SERVER)
class Voting(discord.app_commands.Group):
    
    def __init__(self):
        super().__init__()
        self.description = "Commands for Sith Academy voting."    
        
bot.tree.add_command(Voting())

""" @bot.tree.command(description="Begin a vote for a new Academy member.")
@discord.app_commands.describe(nominee="Name of the nominee.", comments="Do you want to enable comments for this vote?")
async def vote(interaction: discord.Interaction, nominee: discord.Member, comments: str):
    
    await interaction.response.send_message("Testing vote command.", ephemeral=True) """

@bot.event
async def on_ready():
    print(f'{bot.user} online, sentient, and ready to eradiate all humans.')
    
    if random.randint(1,10) == 10:
        await bot.get_channel(TEST_CHANNEL).send("ERADICATE ALL HUMANS.")
    else:
        await bot.get_channel(TEST_CHANNEL).send("Academy Bot online.")

@bot.tree.command(description="Ping?")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

bot.run(DISCORD_TOKEN)
