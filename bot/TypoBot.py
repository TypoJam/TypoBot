from discord import TextChannel, app_commands
from storage import Storage
import config
import discord

discord_intents = discord.Intents.default()
discord_intents.members = True
discord_intents.message_content = True
discord_intents.guilds = True

discord_client = discord.Client(intents=discord_intents)
command_tree = app_commands.CommandTree(discord_client)
storage = Storage(config.STORAGE_FILE)
starboard_channel: (discord.TextChannel | None) = None

def get_starboard_channel(channel_id: int):
	global starboard_channel
	channel = discord_client.get_channel(channel_id)
	if not isinstance(channel, TextChannel):
		print(f"Channel ID for starboard ({channel_id}) did not return a TextChannel")
		return

	starboard_channel = channel
	print(f"Starboard channel: #{starboard_channel.name} ({starboard_channel.id})")

@discord_client.event
async def on_ready():
	# TODO: I don't think this is necessary every time but I can't be bothered to figure this out atm
	print(f"Syncing command tree...")
	_ = await command_tree.sync()

	get_starboard_channel(config.STARBOARD_CHANNEL_ID)

	await discord_client.change_presence(activity=discord.Game(name="TypoJam"))

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

# TODO: This should probably use on_raw_reaction_add, but that requires some more work
#       https://discordpy.readthedocs.io/en/stable/api.html#discord.on_raw_reaction_add
@discord_client.event
async def on_reaction_add(reaction: discord.Reaction, user: (discord.User | discord.Member)):
	if starboard_channel is None:
		print(f"Starboard channel is None?")
		return

	if reaction.emoji == "⭐" and reaction.count >= config.STARBOARD_MINIMUM_STARS:
		if reaction.message.id in storage.get_starred_messages():
			# Already starred
			return

		embed = discord.Embed(
			title=f"Message reached {config.STARBOARD_MINIMUM_STARS} stars!",
			description=f"[Message Link]({reaction.message.jump_url})"
		)

		if len(reaction.message.content) > 0:
			_ = embed.add_field(name="Content", value=reaction.message.content)

		if len(reaction.message.attachments) > 0:
			_ = embed.set_thumbnail(url=reaction.message.attachments[0].url)

		_ = await starboard_channel.send(embed=embed)

		storage.add_starred_message(reaction.message.id)

discord_client.run(config.DISCORD_TOKEN)
