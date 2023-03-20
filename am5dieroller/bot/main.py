#!/usr/bin/env python3
#
# Main file for the die roller bot

import os
from typing import Optional

import discord
from discord import app_commands

from am5dieroller.ars_magica_rolls.stressed import stressed_roll
from am5dieroller.ars_magica_rolls.formulaic import formulaic_roll
from am5dieroller.ars_magica_rolls.spont_rolls import spont_non_roll, fatiguing_spont_roll
from am5dieroller.ars_magica_rolls.simple import simple_roll
#from am5dieroller.ars_magica_rolls.botch import botch_roll


ABOUT = """A simple Ars Magica 5th Edition die roller

Supported commands

/stressed [modifier] - A stressed die (with optional modifier)
/simple [modifier] - A simple die (with optional modifier)
/formulaic <casting_score> <target> - A formulaic spell
/spont <casting_score> <target> - A non-fatiguing spont (no roll, but does the appropriate calculation)
/fspont <casting_score> <target> - A fatiguing spont
/botch <number> - Roll the given number of botch dice

/about - this message

Github Repo: https://github.com/drnlm/Ars_Magica_DieRoller
"""


token = os.environ.get('DISCORD_TOKEN', None)

if not token:
    raise RuntimeError("You must supply a discord token in the environment variable DISCORD_TOKEN")

guilds = os.environ.get('DISCORD_GUILD_IDS', None)
if not guilds:
    print("No DISCORD_GUILD_IDS - the bot will run, but not add any commands")


class DieRollerClient(discord.Client):

    def __init__(self, guild):
        """Create the client and add hooks to sync slash commands"""
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        # Create command tree
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        """Useful logging"""
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def setup_hook(self):
        """Sync commands to the servers we're connected to"""
        for guild_id in guilds.split():
            this_guild =  discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=this_guild)
            await self.tree.sync(guild=this_guild)


client = DieRollerClient(guilds)

# I don't like this idiom for adding commands, but adding commands
# without using the decorator is annoyingly messy

@client.tree.command()
@app_commands.describe(
    modifier="modifier to add to the roll (optional)",
)
async def stressed(interaction: discord.Interaction, modifier: Optional[int] = 0):
    rolls, total, outcome = stressed_roll(modifier)
    if len(rolls) > 1:
        result = f'Rolls: {rolls}. Total (with modifier {modifier}: **{total}**'
    else:
        result = f'Roll: {rolls[0]}. Total (with modifier {modifier}: **{total}**'
    if outcome:
        result += f'\n**{outcome}**\n'
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    modifier="modifier to add to the roll (optional)",
)
async def simple(interaction: discord.Interaction, modifier: Optional[int] = 0):
    rolls, total, outcome = simple_roll(modifier)
    result = f'Roll: {rolls[0]}. Total (with modifier {modifier}: **{total}**'
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura) to add to the roll",
    target="The target level of the spell",
)
async def formulaic(interaction: discord.Interaction, casting_score: int, target: int):
    rolls, total, outcome = formulaic_roll(casting_score, target)
    if len(rolls) > 1:
        result = f'Rolls: {rolls}. Total (with casting score {casting_score}: **{total}** (against {target})'
    else:
        result = f'Roll: {rolls[0]}. Total (with casting score {casting_score}: **{total}** (against {target})'
    result += f'\n**{outcome}**\n'
    await interaction.response.send_message(result)

@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura) to add to the roll",
    target="The target level of the spell",
)
async def spontaneous(interaction: discord.Interaction, casting_score: int, target: int):
    _, total, modified_total, outcome = spont_non_roll(casting_score, target)
    result = f'Total: {total}. Final total **{modified_total}** (against {target})'
    result += f'\n**{outcome}**\n'
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura) to add to the roll",
    target="The target level of the spell",
)
async def fspont(interaction: discord.Interaction, casting_score: int, target: int):
    rolls, total, modified_total, outcome = fatiguing_spont_roll(casting_score, target)
    if len(rolls) > 1:
        result = f'Rolls: {rolls}. Total (with casting score {casting_score}: {total}. Final total **{modified_total}** (against {target})'
    else:
        result = f'Roll: {rolls[0]}. Total (with casting score {casting_score}: {total}. Final total **{modified_total}** (against {target})'
    result += f'\n**{outcome}**\n'
    await interaction.response.send_message(result)


@client.tree.command()
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(ABOUT)


client.run(token)
