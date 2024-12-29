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
need_vote = []
correct = []
incorrect = []
mafia_voted = []
replay = []
queue_limit = 6
mafia_role = "Rat"
mafia_member = None

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
        mafia1_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = f"{interaction.user.mention} you are already in the Mafia!"
        )

        await interaction.response.send_message(embed = mafia1_embed)
    elif len(queue) >= queue_limit:
        mafia2_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = "The Mafia is full! Please wait for the next game."
        )

        await interaction.response.send_message(embed = mafia2_embed)
    else:
        queue.append(interaction.user)
        need_vote.append(interaction.user)
        queue_mentions = " ".join(player.mention for player in queue)
        mafia3_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = f"{interaction.user.mention} has joined the Mafia! ({len(queue)}/{queue_limit})\n\n**Current Mafia**\n{queue_mentions}"
        )

        await interaction.response.send_message(embed = mafia3_embed)
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
    global need_vote
    if member in queue:
        mafia4_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = f"{member.mention} is already in the Mafia!"
        )

        await interaction.response.send_message(embed = mafia4_embed)
    elif len(queue) >= queue_limit:
        mafia5_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = "The Mafia is full! Please wait for the next game."
        )

        await interaction.response.send_message(embed = mafia5_embed)
    else:
        queue.append(member)
        need_vote.append(member)
        queue_mentions = " ".join(player.mention for player in queue)
        mafia6_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = f"{member.mention} has joined the Mafia! ({len(queue)}/{queue_limit})\n\n**Current Mafia**\n{queue_mentions}"
        )

        await interaction.response.send_message(embed = mafia6_embed)
        if len(queue) == queue_limit:
            await start_game()

@tree.command(
    name="leave",
    description="Leave the Mafia",
    guild=discord.Object(id=271191981999259648)
)
async def leave(interaction):
    global queue
    global need_vote
    if interaction.user in queue:
        queue.remove(interaction.user)
        need_vote.remove(interaction.user)
        queue_mentions = " ".join(player.mention for player in queue)
        leave1_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = f"{interaction.user.mention} has left the Mafia. ({len(queue)}/{queue_limit})\n\n**Current Mafia**\n{queue_mentions}"
        )

        await interaction.response.send_message(embed = leave1_embed)
    else:
        leave2_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = f"{interaction.user.mention}, you are not in the Mafia!"
        )

        await interaction.response.send_message(embed = leave2_embed)

@tree.command(
    name="rules",
    description="How to play",
    guild=discord.Object(id=271191981999259648)
)
async def rules(interaction):
    rules_embed = discord.Embed(
        color = discord.Colour.from_rgb(255, 0, 0),
        title = "Boss of the Mob",
        description = "HOW TO PLAY"
    )

    await interaction.response.send_message(embed = rules_embed)

async def start_game():
    global queue
    global mafia_member
    channel = client.get_channel(1321380377461522443)
    if len(queue) != queue_limit:
        start1_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = "The Mafia is not fully staffed!"
        )

        await channel.send(embed = start1_embed)
        return

    start2_embed = discord.Embed(
        color = discord.Colour.from_rgb(255, 0, 0),
        title = "Boss of the Mob",
        description = "The game is starting! Teams are being assigned..."
    )

    await channel.send(embed = start2_embed)

    # Shuffle players and assign teams
    random.shuffle(queue)
    team1 = queue[:3]
    team2 = queue[3:]

    # Select the Mafia Rat
    mafia_member = random.choice(queue)

    # Notify Mafia in DM
    start3_embed = discord.Embed(
        color = discord.Colour.from_rgb(255, 0, 0),
        title = "Boss of the Mob",
        description = f"You are the {mafia_role}! Your job is to subtly sabotage your team."
    )

    await mafia_member.send(embed = start3_embed)

    # Announce teams
    team1_mentions = "\n".join(player.mention for player in team1)
    team2_mentions = "\n".join(player.mention for player in team2)

    start4_embed = discord.Embed(
        color = discord.Colour.from_rgb(255, 0, 0),
        title = "Boss of the Mob"
    )

    start4_embed.add_field(name = "**Team 1**", value = f"{team1_mentions}", inline = True)
    start4_embed.add_field(name = "**Team 2**", value = f"{team2_mentions}", inline = True)
    start4_embed.set_footer(text = "There's a Rat in the family... Find him... Make him sleep with the fishes...")
    await channel.send(embed = start4_embed)

    # Reset the queue
    # queue = []

@tree.command(
    name="report",
    description="Report to the Boss",
    guild=discord.Object(id=271191981999259648)
)
async def report(interaction: discord.Interaction, member: discord.Member):
    global queue
    global queue_limit
    global correct
    global incorrect
    global mafia_member
    global need_vote
    global mafia_voted
    global replay
    channel = client.get_channel(1321380377461522443)
    if interaction.user in need_vote:
        if mafia_member == member:
            mafia_voted.append(interaction.user.mention)
            replay.append(interaction.user.mention)
            need_vote.remove(interaction.user)
            queue_mentions = " ".join(player.mention for player in need_vote)
            correct.append(interaction.user.mention)
            correct_mentions = "\n".join(correct)
            incorrect_mentions = "\n".join(incorrect)
            report1_embed = discord.Embed(
                color = discord.Colour.from_rgb(255, 0, 0),
                title = "Boss of the Mob",
                description = f"**Awaiting ({len(queue) - len(mafia_voted)}/{queue_limit})**\n{queue_mentions}"
            )
            await interaction.response.send_message(embed = report1_embed)
            if len(correct) + len(incorrect) == queue_limit:
                report2_embed = discord.Embed(
                    color = discord.Colour.from_rgb(255, 0, 0),
                    title = "Boss of the Mob"
                )
                report2_embed.add_field(name = "**Correct**", value = f"{correct_mentions}", inline = True)
                report2_embed.add_field(name = "**Incorrect**", value = f"{incorrect_mentions}", inline = True)
                report2_embed.add_field(name = "", value = f"The Rat was {mafia_member.mention}", inline = False)
                await channel.send(embed = report2_embed)
                queue = []
                need_vote = []
                correct = []
                incorrect = []
                mafia_voted = []
        elif mafia_member != member:
            mafia_voted.append(interaction.user.mention)
            replay.append(interaction.user.mention)
            need_vote.remove(interaction.user)
            queue_mentions = " ".join(player.mention for player in need_vote)
            incorrect.append(interaction.user.mention)
            correct_mentions = "\n".join(correct)
            incorrect_mentions = "\n".join(incorrect)
            report3_embed = discord.Embed(
                color = discord.Colour.from_rgb(255, 0, 0),
                title = "Boss of the Mob",
                description = f"**Awaiting ({len(queue) - len(mafia_voted)}/{queue_limit})**\n{queue_mentions}"
            )
            await interaction.response.send_message(embed = report3_embed)
            if len(correct) + len(incorrect) == queue_limit:
                report4_embed = discord.Embed(
                    color = discord.Colour.from_rgb(255, 0, 0),
                    title = "Boss of the Mob"
                )
                report4_embed.add_field(name = "**Correct**", value = f"{correct_mentions}", inline = True)
                report4_embed.add_field(name = "**Incorrect**", value = f"{incorrect_mentions}", inline = True)
                report4_embed.add_field(name = "", value = f"The Rat was {mafia_member.mention}", inline = False)
                await channel.send(embed = report4_embed)
                queue = []
                need_vote = []
                correct = []
                incorrect = []
                mafia_voted = []
    elif interaction.user in queue:
        if interaction.user not in need_vote:
            report5_embed = discord.Embed(
                color = discord.Colour.from_rgb(255, 0, 0),
                title = "Boss of the Mob",
                description = f"{interaction.user.mention} you have already submitted your report."
            )
            await interaction.response.send_message(embed = report5_embed)
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you cannot submit a report if you are not in the Mafia!")
    # if len(correct) + len(incorrect) == queue_limit:
    #     report5_embed = discord.Embed(
    #         color = discord.Colour.from_rgb(255, 0, 0),
    #         title = "Boss of the Mob"
    #     )
    #     report5_embed.add_field(name = "**Correct**", value = f"{correct_mentions}", inline = True)
    #     report5_embed.add_field(name = "**Incorrect**", value = f"{incorrect_mentions}", inline = True)
    #     report5_embed.add_field(name = "", value = f"The Rat was {mafia_member.mention}", inline = False)
    #     await channel.send(embed = report5_embed)
    #     queue = []
    #     mafia_voted = []

# @tree.command(
#     name="requeue",
#     description="Requeue all Mafia",
#     guild=discord.Object(id=271191981999259648)
# )
# async def requeue(interaction):
#     global queue
#     global replay
#     if len(queue) > 0:
#         requeue1_embed = discord.Embed(
#             color = discord.Colour.from_rgb(255, 0, 0),
#             title = "Boss of the Mob",
#             description = "There are new Mafia in the queue, please requeue manually."
#         )
#         await interaction.response.send_message(embed = requeue1_embed)
#     else:
#         queue.append(player.mention for player in replay)
#         replay = []
#         need_vote.append(player for player in replay)
#         if len(queue) == queue_limit:
#             await start_game()

@tree.command(
    name="status",
    description="View the Mafia",
    guild=discord.Object(id=271191981999259648)
)
async def status(interaction):
    if not queue:
        status1_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = "The Mafia is currently unstaffed."
        )

        await interaction.response.send_message(embed = status1_embed)
    else:
        queue_mentions = " ".join(player.mention for player in queue)
        status2_embed = discord.Embed(
            color = discord.Colour.from_rgb(255, 0, 0),
            title = "Boss of the Mob",
            description = f"Current Mafia ({len(queue)}/{queue_limit}): {queue_mentions}"
        )

        await interaction.response.send_message(embed = status2_embed)

# UPDATE TOKEN IN ENV FILE / TOP OF FILE
client.run(TOKEN)
