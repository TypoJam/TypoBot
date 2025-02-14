from . import config
from .storage import Storage
from discord import app_commands
from discord.ext import commands
import discord

class Starboard(commands.Cog):
    def __init__(self, bot: commands.Bot, storage: Storage, starboard_channel: (discord.TextChannel | None)):
        self.bot: commands.Bot = bot
        self.storage: Storage = storage
        self.starboard_channel: (discord.TextChannel | None) = starboard_channel

        force_star_context: app_commands.ContextMenu = app_commands.ContextMenu(
            name="Force Star",
            callback=self.force_star
        )
        self.bot.tree.add_command(force_star_context)

    async def _star_message(self, message: discord.Message, title: str) -> None:
        if self.starboard_channel is None:
            print("Starboard channel is None?")
            return

        # TODO: Use Discord's forward message feature instead of copying the content
        embed = discord.Embed(
            title=title,
            description=f"[Message Link]({message.jump_url})\nBy {message.author.mention}"
        )

        if len(message.content) > 0:
            _ = embed.add_field(name="Content", value=message.content)

        if len(message.attachments) > 0:
            _ = embed.set_thumbnail(url=message.attachments[0].url)

        _ = await self.starboard_channel.send(embed=embed)

        self.storage.add_starred_message(message.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        STAR = "⭐"
        if payload.emoji.name != STAR:
            return

        assert self.bot.user is not None # Shut LSP up
        if payload.user_id == self.bot.user.id:
            return

        if payload.message_id in self.storage.get_starred_messages():
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        message = await channel.fetch_message(payload.message_id)
        stars = [ r for r in message.reactions if r.emoji == STAR].pop().count
        if stars < config.STARBOARD_MINIMUM_STARS:
            return

        await self._star_message(message, f"Message reached {config.STARBOARD_MINIMUM_STARS} stars!")

    @app_commands.checks.has_permissions(administrator=True)
    async def force_star(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer()

        if interaction.guild is None:
            await interaction.followup.send("This command can only be ran in a server")
            return

        await self._star_message(message, f"Message was force starred by @{interaction.user.name}")
        await interaction.followup.send(f"Starred message by @{message.author.name}")
