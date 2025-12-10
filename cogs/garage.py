from discord import app_commands
import discord
from discord.ext import commands
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
            embed.add_field(name=car["name"], value=f"Rareté : {car['rarity']}\nValeur : {car['price']} 💰", inline=False)

        await interaction.response.send_message(embed=embed)

    # ------------------- NOUVELLE COMMANDE -------------------
    @app_commands.command(name="carinfo", description="Voir les infos détaillées d'une voiture.")
    async def carinfo(self, interaction: discord.Interaction, car_id: str):
        cars = self.load_cars()

        if car_id not in cars:
            await interaction.response.send_message("⚠️ Voiture introuvable.")
            return

        car = cars[car_id]
        embed = discord.Embed(
            title=f"🏎️ Infos sur {car['name']}",
            color=discord.Color.purple()
        )
        embed.add_field(name="Rareté", value=car["rarity"], inline=True)
        embed.add_field(name="Prix de base", value=f"{car['price']} 💰", inline=True)
        embed.add_field(name="Appréciation", value=f"{car['appreciation']*100}% par enchère", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Garage(bot))
