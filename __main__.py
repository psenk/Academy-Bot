import logging
import os
import random
from typing import List

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from dotenv import load_dotenv

from utils.QueryTool import QueryTool

load_dotenv(override=True)


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


TEST_CHANNEL = 986537383250001940
TEST_SERVER = discord.Object(id=969399636995493899)
TEST_ACADEMY_ROLE = 1268612663039098951
TEST_OVERSEER_ROLE = 1265728711731183759

bot_logger = logging.getLogger(__name__)
bot_logger.addHandler(logging.FileHandler(
    filename="logs/bot.log", encoding='utf-8', mode='w'))
bot_logger.setLevel(logging.DEBUG)


# TODO: create list of who hasn't voted in specific vote
# TODO: create list of who voted for what
# TODO: multiple votes at once
# IDEA: nomination entity, list of votes/voters/comments, nominee name, comments bool?
# TODO: reminder to vote ping command
# TODO: reminder to vote DM command
# IDEA: easy to use!!! help command, good descriptions

# ? # ? # ACADEMY COMMANDS # ? # ? #

@bot.tree.command(description='Submit your choice in an Academy vote.')
@app_commands.describe(vote='What are you voting on?')
@app_commands.checks.has_role(TEST_ACADEMY_ROLE)
@app_commands.guilds(TEST_SERVER)
async def avote(interaction: discord.Interaction, vote: int) -> None:
    """
    # SELECT AN ACTIVE VOTING PERIOD
    # SELECT OPTIONS
    # SEND VOTE
    """
    pass

@avote.autocomplete('vote')
async def auto_complete_vote(interaction: discord.Interaction, current: str) -> List[Choice]:
    async with QueryTool() as tool:
        day = await tool.get_day()
    bot_logger.info(f'\nDay from database -> {day}')
    
    choices = [choice for choice in Choices.DAY_AND_BOARD if choice.value <= day]
    bot_logger.info(f'Auto-complete days options -> {choices}')
    return choices


@bot.tree.command(description='Shows this help menu.')
@app_commands.checks.has_role(TEST_ACADEMY_ROLE)
@app_commands.guilds(TEST_SERVER)
async def ahelp(interaction: discord.Interaction) -> None:
    """
    # SHOW HELP EMBED
    """
    pass


# ? # ? # OVERSEER ONLY COMMANDS # ? # ? #


@bot.tree.command(description='OVERSEER: Create a new vote.')
@app_commands.checks.has_role(TEST_OVERSEER_ROLE)
@app_commands.describe(vote='Title of vote', description='Description of vote', period='Length of vote (optional)')
@app_commands.guilds(TEST_SERVER)
async def acreate(interaction: discord.Interaction, vote: str, description: str, period: int = 14) -> None:
    """
    Create a voting period.
    param interaction: Discord Interaction instance
    param vote: str, name of voting period
    param description: str, description of voting period
    param period: int, optional, set length of time of vote
    return: None
    """
    pass


@bot.tree.command(description='OVERSEER: Delete a specific vote from a voting period.')
@app_commands.checks.has_role(TEST_OVERSEER_ROLE)
@app_commands.describe(vote='Name of voting period', name='Vote to remove')
@app_commands.guilds(TEST_SERVER)
async def adeletevote(interaction: discord.Interaction, vote: int, name: int) -> None:
    """
    Delete a single vote from a voting period.
    param interaction: Discord Interaction instance
    param vote: voting period to access
    param name: vote to remove
    return: None
    """
    
    """
    # WARN
    # DELETE ONE VOTE
    """
    pass

@adeletevote.autocomplete('vote')
async def auto_complete_vote(interaction: discord.Interaction, current: str) -> List[Choice]:
    # QUERY
    bot_logger.info(f'REPLACE')
    
    #choices = [choice for choice in Choices.DAY_AND_BOARD if choice.value <= day]
    bot_logger.info(f'REPLACE')
    return

@adeletevote.autocomplete('name')
async def auto_complete_vote(interaction: discord.Interaction, current: str) -> List[Choice]:
    # QUERY
    bot_logger.info(f'REPLACE')
    
    #choices = [choice for choice in Choices.DAY_AND_BOARD if choice.value <= day]
    bot_logger.info(f'REPLACE')
    return


@bot.tree.command(description='OVERSEER: Delete a voting period.')
@app_commands.checks.has_role(TEST_OVERSEER_ROLE)
@app_commands.describe(vote='Name of voting period')
@app_commands.guilds(TEST_SERVER)
async def adeleteperiod(interaction: discord.Interaction, vote: ) -> None:
    """
    # WARN
    # DELETE VOTING PERIOD
    """
    pass


@bot.tree.command(description='Show status of current vote.')
@app_commands.describe(vote='Name of voting period.')
@app_commands.guilds(TEST_SERVER)
async def astatus(interaction: discord.Interaction, name: discord.Member) -> None:
    """
    # GET VOTING PERIOD
    # COMPARE WITH LIST OF ACADEMY MEMBERS
    # SHOW EMBED OUTPUT
    """
    pass


@bot.tree.command(description='Show status of current vote.')
@app_commands.describe(vote='Name of voting period.')
@app_commands.guilds(TEST_SERVER)
async def aping(interaction: discord.Interaction, name: discord.Member) -> None:
    """
    # REMIND MEMBERS TO VOTE
    """
    pass



@bot.event
async def on_ready():
    print(f'{bot.user} online, sentient, and ready to eradiate all humans.')
    await bot.tree.sync(guild=TEST_SERVER)

    if random.randint(1, 9) == 10:
        await bot.get_channel(TEST_CHANNEL).send("ERADICATE ALL HUMANS.")
    else:
        await bot.get_channel(TEST_CHANNEL).send("Academy Bot online.")



bot.run(DISCORD_TOKEN, log_handler=logging.FileHandler(
    filename='logs/discord.log', encoding='utf-8', mode='w'), log_level=logging.DEBUG)
