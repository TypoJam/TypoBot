from discord import app_commands
from discord.ext import commands
from .storage import Storage
from . import config
import discord
from . import starboard

discord_intents = discord.Intents.default()
discord_intents.members = True
discord_intents.message_content = True
discord_intents.guilds = True

bot = commands.Bot(command_prefix="=", intents=discord_intents)
storage = Storage(config.STORAGE_FILE)

def get_starboard_channel(channel_id: int):
	channel = bot.get_channel(channel_id)
	if not isinstance(channel, discord.TextChannel):
		print(f"Channel ID for starboard ({channel_id}) did not return a TextChannel")
		return

	return channel

@bot.event
async def on_ready():
	starboard_channel: (discord.TextChannel | None) = get_starboard_channel(config.STARBOARD_CHANNEL_ID)
	await bot.add_cog(starboard.Starboard(bot, storage, starboard_channel))

	await bot.change_presence(activity=discord.Game(name="TypoJam"))

	# TODO: I don't think this is necessary every time but I can't be bothered to figure this out atm
	print(f"Syncing command tree...")
	_ = await bot.tree.sync()

	print(f"Discord client ready.")

@bot.tree.error
async def command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
	assert interaction.command is not None
	await interaction.followup.send(
		f"An error occurred while executing `{interaction.command.name}`:\n```{error}```"
	)

@bot.event
async def on_member_join(member: discord.Member):
	if not config.JOIN_LEAVE_MESSAGE:
		return

	if member.guild.system_channel is None:
		return

	_ = await member.guild.system_channel.send(f"`{member.id}` {member.mention} Joined!")

@bot.event
async def on_member_remove(member: discord.Member):
	if not config.JOIN_LEAVE_MESSAGE:
		return

	if member.guild.system_channel is None:
		return

	_ = await member.guild.system_channel.send(f"`{member.id}` @{member.name} Left")

@bot.event
async def on_thread_create(thread: discord.Thread):
	message = await thread.fetch_message(thread.id)
	await message.pin(reason="First message in thread")

bot.run(config.DISCORD_TOKEN)
