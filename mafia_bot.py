import discord
from discord import app_commands
import random
import os
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN: str = os.getenv('TOKEN')

# Bot setup
intents = discord.Intents.all()
intents.messages = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Game state
queue = []
queue_limit = 6
mafia_role = "Rat"

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=271191981999259648))
    print(f'Bot is ready as {client.user}')

@tree.command(
    name="mafia",
    description="Join the Mafia",
    guild=discord.Object(id=271191981999259648)
)
async def mafia(interaction):
    global queue
    if interaction.user in queue:
        await interaction.response.send_message(f"{interaction.user.mention}, you are already in the Mafia!")
    elif len(queue) >= queue_limit:
        await interaction.response.send_message("The Mafia is full! Please wait for the next game.")
    else:
        queue.append(interaction.user)
        await interaction.response.send_message(f"{interaction.user.mention} has joined the Mafia! ({len(queue)}/{queue_limit})")
        if len(queue) == queue_limit:
            await start_game()

@tree.command(
    name="addmafia",
    description="Add someone to the Mafia",
    guild=discord.Object(id=271191981999259648)
)
@discord.app_commands.checks.has_role(764088348452323348)
async def addmafia(interaction: discord.Interaction, member: discord.Member):
    global queue
    if member in queue:
        await interaction.response.send_message(f"{member.mention} is already in the Mafia!")
    elif len(queue) >= queue_limit:
        await interaction.response.send_message("The Mafia is full! Please wait for the next game.")
    else:
        queue.append(member)
        await interaction.response.send_message(f"{member.mention} has joined the Mafia! ({len(queue)}/{queue_limit})")
        if len(queue) == queue_limit:
            await start_game()

@tree.command(
    name="leave",
    description="Leave the Mafia",
    guild=discord.Object(id=271191981999259648)
)
async def leave(interaction):
    global queue
    if interaction.user in queue:
        queue.remove(interaction.user)
        await interaction.response.send_message(f"{interaction.user.mention} has left the Mafia. ({len(queue)}/{queue_limit})")
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you are not in the Mafia!")

@tree.command(
    name="rules",
    description="How to play",
    guild=discord.Object(id=271191981999259648)
)
async def rules(interaction):
    await interaction.response.send_message("HOW TO PLAY")

async def start_game():
    global queue
    channel = client.get_channel(1321380377461522443)
    if len(queue) != queue_limit:
        await channel.send("The Mafia is not fully staffed!")
        return

    await channel.send("The game is starting! Teams are being assigned...")

    # Shuffle players and assign teams
    random.shuffle(queue)
    team1 = queue[:3]
    team2 = queue[3:]

    # Select the Mafia Rat
    mafia_member = random.choice(queue)

    # Notify Mafia in DM
    await mafia_member.send(f"You are the {mafia_role}! Your job is to subtly sabotage your team.")

    # Announce teams
    team1_mentions = ", ".join(player.mention for player in team1)
    team2_mentions = ", ".join(player.mention for player in team2)

    await channel.send(f"Team 1: {team1_mentions}\nTeam 2: {team2_mentions}")

    # Reset the queue
    queue = []

@tree.command(
    name="status",
    description="View the Mafia",
    guild=discord.Object(id=271191981999259648)
)
async def status(interaction):
    if not queue:
        await interaction.response.send_message("The Mafia is currently unstaffed.")
    else:
        queue_mentions = ", ".join(player.mention for player in queue)
        await interaction.response.send_message(f"Current Mafia ({len(queue)}/{queue_limit}): {queue_mentions}")

# UPDATE TOKEN IN ENV FILE / TOP OF FILE
client.run(TOKEN)
