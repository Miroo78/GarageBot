import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    await tree.sync()
    print("Slash commandes synchronisées.")


# Chargement des cogs
async def load_cogs():
    await bot.load_extension("cogs.economy")
    await bot.load_extension("cogs.shop")
    await bot.load_extension("cogs.garage")
    await bot.load_extension("cogs.auction")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())
