import discord
from discord.ext import commands
from discord import app_commands
import json

class Garage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_users(self):
        with open("data/users.json", "r") as f:
            return json.load(f)

    def load_cars(self):
        with open("data/cars.json", "r") as f:
            return json.load(f)

    @app_commands.command(name="garage", description="Voir toutes tes voitures.")
    async def garage(self, interaction: discord.Interaction):
        users = self.load_users()
        cars = self.load_cars()
        uid = str(interaction.user.id)

        if uid not in users:
            await interaction.response.send_message("Utilise /start d’abord.")
            return

        garage = users[uid]["garage"]

        if not garage:
            await interaction.response.send_message("Ton garage est vide.")
            return

        embed = discord.Embed(title="🚗 Ton Garage")

        for cid in garage:
            car = cars[cid]
            embed.add_field(name=car["name"], value=f"Rareté : {car['rarity']}", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Garage(bot))
