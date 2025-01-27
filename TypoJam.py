from discord import app_commands
import discord
import config

discord_intents = discord.Intents.default()
discord_intents.members = True
discord_intents.message_content = True
discord_intents.guilds = True

discord_client = discord.Client(intents=discord_intents)
command_tree = app_commands.CommandTree(discord_client)

@discord_client.event
async def on_ready():
	# TODO: I don't think this is necessary every time but I can't be bothered to figure this out atm
	print(f"Syncing command tree...")
	_ = await command_tree.sync()

	print(f"Discord client ready.")

# Some error handling so your bot doesn't freeze on 'bot is thinking...'
@command_tree.error
async def command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
	assert interaction.command is not None
	await interaction.followup.send(
		f"An error occurred while executing `{interaction.command.name}`:\n```{error}```"
	)

@discord_client.event
async def on_member_join(member: discord.Member):
	if member.guild.system_channel is None:
		return

	_ = await member.guild.system_channel.send(f"`{member.id}` {member.mention} Joined!")

@discord_client.event
async def on_member_remove(member: discord.Member):
	if member.guild.system_channel is None:
		return

	_ = await member.guild.system_channel.send(f"`{member.id}` @{member.name} Left")

@discord_client.event
async def on_thread_create(thread: discord.Thread):
	message = await thread.fetch_message(thread.id)
	await message.pin(reason="First message in thread")

discord_client.run(config.DISCORD_TOKEN)
