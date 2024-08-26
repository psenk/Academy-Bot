import discord
from discord.ext.commands import Bot
import datetime
import json

from tools.QueryTool import QueryTool
from utils import Functions

CHARACTER_LIMIT = 500


class VotingBooth(discord.ui.View):

    def __init__(self, bot: Bot, interaction: discord.Interaction, overseer: str, period: list) -> None:
        """
        Constructor for VotingBooth
        """
        super().__init__(timeout=60.0)
        self.logger = Functions.create_logger('votingbooth')
        self.bot = bot
        self.interaction = interaction
        self.overseer = overseer
        self.period = period
        self.id = period[0]
        self.message: discord.Message = None
        self.vote = {
            'name': f'{interaction.user.display_name}'
        }

        # ! HAS VOTED??
        # ! CONFIRMATION WINDOW?

    async def create(self) -> None:
        """
        Creates VotingBooth embed.
        return: None
        """

        img = discord.File("pics\\avatar.jpg")
        voting_booth = discord.Embed(
            title="Voting Booth", color=0xFF0000, description="Submit your vote below!  Comments may be provided after vote has been submitted."
        )
        voting_booth.set_thumbnail(url='attachment://avatar.jpg')
        voting_booth.set_author(name=f'Sith Overseer: {self.overseer}')
        voting_booth.add_field(
            name='Title', value=f'{self.period["title"]}', inline=True)
        voting_booth.add_field(
            name='Nominee', value=f'{self.period["nominee"]}', inline=True)
        voting_booth.add_field(name='', value='', inline=True)
        voting_booth.add_field(name='Overseer Comments',
                               value=f'{self.period["comments"]}', inline=True)
        self.message = await self.interaction.followup.send(embed=voting_booth, view=self, file=img, ephemeral=True)
        self.logger.info(f'Voting booth embed posted for -> {self.interaction.user.display_name}')

    @discord.ui.button(label="Approve", emoji="👍", style=discord.ButtonStyle.green)
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.vote['vote'] = True
        await self.comments(interaction)

    @discord.ui.button(label="Reject", emoji="👎", style=discord.ButtonStyle.red)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        self.vote['vote'] = False        
        await self.comments(interaction)

    async def get_vote(self) -> dict:
        return self.vote

    async def comments(self, interaction: discord.Interaction) -> None:
        class YesNoButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30.0)
                self.choice = None

            @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
            async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer()
                self.choice = True
                self.stop()

            @discord.ui.button(label='No', style=discord.ButtonStyle.red)
            async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.choice = False
                await interaction.response.defer()
                self.stop()

        confirmation = YesNoButtons()
        comments_message = await interaction.followup.send("Would you like to add any comments to your vote?", view=confirmation, ephemeral=True)
        await confirmation.wait()

        if confirmation.choice:
            true_message = await interaction.followup.send("Please post your comments below.", ephemeral=True)
            while True:
                response = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user and m.channel == interaction.channel, timeout=60.0)
                if len(response.content) > CHARACTER_LIMIT:
                    await interaction.followup.send(f"You had way too much to say! Please keep your comments under {CHARACTER_LIMIT} characters.  Your response was {len(response.content)} characters long!")
                else:
                    break
            self.vote['comments'] = response.content
            await response.delete()
            await true_message.delete()
        else:
            self.vote['comments'] = None
        self.vote['time'] = datetime.datetime.now().strftime(
            "%m/%d/%Y, %H:%M:%S")
        await self.submit()
        await self.message.delete()
        await comments_message.delete()
        self.logger.info("Comments function completed.")

    async def submit(self):
        vote = json.dumps(self.vote)
        print(vote)
        async with QueryTool() as tool:
           await tool.submit_vote(vote, self.id)
        self.logger.info(f'Vote submitted to database -> {vote}')
        response = await self.interaction.followup.send("Your vote has been submitted!")
        await response.add_reaction('✅')
        await response.delete(delay=10.0)
