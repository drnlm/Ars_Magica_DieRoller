#!/usr/bin/env python3
#
# Main file for the die roller bot

"""Implementation of the actual bot"""

import os
from typing import Optional

import discord
from discord import app_commands

from .internal import (stressed_internal, simple_internal, botch_internal,
                       formulaic_internal, formulaic_simple_internal,
                       ritual_internal, spontaneous_internal, fspont_internal)


ABOUT = """A simple Ars Magica 5th Edition die roller

Supported commands

/stressed [modifier] - A stressed die (with optional modifier)
/simple [modifier] - A simple die (with optional modifier)
/formulaic <casting_score> <target> - A formulaic spell using a stressed die
/formulaic_simple <casting_score> <target> - A formulaic spell using a simple die
/ritual <casting_score> <target> - A ritual spell using a stressed die
/spontaneous <casting_score> <target> - A non-fatiguing spont (no roll, but does the appropriate calculation)
/fspont <casting_score> <target> - A fatiguing spont
/botch <number> - Roll the given number of botch dice

/about - this message

Github Repo: https://github.com/drnlm/Ars_Magica_DieRoller
"""


token = os.environ.get('DISCORD_TOKEN', None)

if not token:
    raise RuntimeError("You must supply a discord token in the environment variable DISCORD_TOKEN")


class DieRollerClient(discord.Client):
    """The client used by bot"""

    def __init__(self):
        """Create the client and add hooks to sync slash commands"""
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        # Create command tree
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        """Useful logging"""
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def setup_hook(self):
        """Sync commands"""
        await self.tree.sync()


client = DieRollerClient()


# I don't like this idiom for adding commands, but adding commands
# without using the decorator is annoyingly messy

# The actual tree commands

@client.tree.command()
@app_commands.describe(
    modifier="modifier to add to the roll (optional)",
)
async def stressed(interaction: discord.Interaction, modifier: Optional[int] = 0):
    """A stressed die roll"""
    result = stressed_internal(modifier)
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    modifier="modifier to add to the roll (optional)",
)
async def simple(interaction: discord.Interaction,
                 modifier: Optional[ app_commands.Range[int, 0, None] ] = 0):
    """A simple die roll - no botch, no open end"""
    result = simple_internal(modifier)
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    number="number of dice to roll (optional, defaults to 1)",
)
async def botch(interaction: discord.Interaction,
                number: Optional[ app_commands.Range[int, 1, None] ] = 1):
    """Roll for a possible botch"""
    result = botch_internal(number)
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura) to add to the roll",
    target="The target level of the spell",
)
async def formulaic(interaction: discord.Interaction,
                    casting_score: app_commands.Range[int, 0, None],
                    target: app_commands.Range[int, 0, None]):
    """A formulaic spell using a stressed die"""
    result = formulaic_internal(casting_score, target)
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura) to add to the roll",
    target="The target level of the spell",
)
async def formulaic_simple(interaction: discord.Interaction,
                           casting_score: app_commands.Range[int, 0, None],
                           target: app_commands.Range[int, 0, None]):
    """A formulaic spell using a simple die"""
    result = formulaic_simple_internal(casting_score, target)
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura + Artes Liberales + Philosophiae) to add to the roll",
    target="The target level of the spell",
)
async def ritual(interaction: discord.Interaction,
                 casting_score: app_commands.Range[int, 0, None],
                 target: app_commands.Range[int, 0, None]):
    """A ritual spell using a stressed die"""
    result = ritual_internal(casting_score, target)
    await interaction.response.send_message(result)



@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura) to add to the roll",
    target="The target level of the spell",
)
async def spontaneous(interaction: discord.Interaction,
                      casting_score: app_commands.Range[int, 0, None],
                      target: app_commands.Range[int, 0, None]):
    """A non-fatiguing spontaneous spell (no die roll, divide total by 5)"""
    result = spontaneous_internal(casting_score, target)
    await interaction.response.send_message(result)


@client.tree.command()
@app_commands.describe(
    casting_score="The casting score (Stamina + Art + Form + Aura) to add to the roll",
    target="The target level of the spell",
)
async def fspont(interaction: discord.Interaction,
                 casting_score: app_commands.Range[int, 0, None],
                 target: app_commands.Range[int, 0, None]):
    """A fatiguing spontaneous spell (stressed die roll, divide total by 2)"""
    result = fspont_internal(casting_score, target)
    await interaction.response.send_message(result)


@client.tree.command()
async def about(interaction: discord.Interaction):
    """Help about the Ars Magica die roller"""
    await interaction.response.send_message(ABOUT)


client.run(token)
