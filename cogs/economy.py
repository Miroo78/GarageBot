import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_users(self):
        with open("data/users.json", "r") as f:
            return json.load(f)

    def save_users(self, data):
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

    @app_commands.command(name="start", description="Créer ton profil joueur.")
    async def start(self, interaction: discord.Interaction):
        users = self.load_users()
        uid = str(interaction.user.id)

        if uid in users:
            await interaction.response.send_message("Tu as déjà un profil.", ephemeral=True)
            return

        users[uid] = {"money": 500, "garage": []}
        self.save_users(users)

        await interaction.response.send_message("Profil créé ! Tu commences avec 500 crédits.")

    @app_commands.command(name="daily", description="Récupérer ton bonus quotidien.")
    async def daily(self, interaction: discord.Interaction):
        users = self.load_users()
        uid = str(interaction.user.id)

        if uid not in users:
            await interaction.response.send_message("Utilise /start d’abord.")
            return

        users[uid]["money"] += 500
        self.save_users(users)

        await interaction.response.send_message("Tu as gagné 500 crédits aujourd'hui.")

    @app_commands.command(name="balance", description="Voir ton solde.")
    async def balance(self, interaction: discord.Interaction):
        users = self.load_users()
        uid = str(interaction.user.id)

        if uid not in users:
            await interaction.response.send_message("Utilise /start d’abord.")
            return

        money = users[uid]["money"]
        await interaction.response.send_message(f"Tu as **{money} crédits**.")


async def setup(bot):
    await bot.add_cog(Economy(bot))
