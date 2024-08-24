import discord

from utils import Functions


class VotingBooth(discord.ui.View):

    def __init__(self, interaction: discord.Interaction, overseer: str) -> None:
        """
        Constructor for VotingBooth
        """
        super().__init__(timeout=60.0)
        self.logger = Functions.create_logger('votingbooth')
        self.interaction = interaction
        self.overseer = overseer

    async def create_voting_booth_embed(self) -> None:
        """
        Creates VotingBooth embed.
        return: None
        """
        
        # get voting period info (need title, nominee, comments)
        img = discord.File("pics\\avatar.jpg")
        voting_booth = discord.Embed(
            title="Voting Booth", color=0xFF0000, description="Submit your vote below!  Comments may be provided after vote has been submitted."
        )
        # title
        # nominee (if statement)
        # overseer comments
        voting_booth.set_thumbnail(url="attachment://avatar.jpg")
        voting_booth.set_author(name=f"Sith Overseer: {self.overseer}")
        voting_booth.add_field(name='Title', value='', inline=True)
        voting_booth.add_field(name='Nominee', value='', inline=True)
        voting_booth.add_field(name='', value='', inline=True)
        voting_booth.add_field(name='Overseer Comments', value='', inline=True)
        await self.interaction.followup.send(embed=voting_booth, view=self, file=img)
        

    @discord.ui.button(label="Approve", emoji="👍", style=discord.ButtonStyle.green)
    async def approve_button(self, interaction: discord.Interaction):
        await interaction.response.defer()

    @discord.ui.button(label="Reject", emoji="👎", style=discord.ButtonStyle.red)
    async def reject_button(self, interaction: discord.Interaction):
        await interaction.response.defer()
