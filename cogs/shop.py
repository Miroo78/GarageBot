import discord
from discord.ext import commands
from discord import app_commands
import json

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_cars(self):
        with open("data/cars.json", "r") as f:
            return json.load(f)

    def load_users(self):
        with open("data/users.json", "r") as f:
            return json.load(f)

    def save_users(self, data):
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

    @app_commands.command(name="shop", description="Voir les voitures disponibles.")
    async def shop(self, interaction: discord.Interaction):
        cars = self.load_cars()
        embed = discord.Embed(title="Boutique des voitures de collection")

        for cid, car in cars.items():
            embed.add_field(
                name=f"{car['name']} ({cid})",
                value=f"Prix : {car['price']} crédits\nRareté : {car['rarity']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Acheter une voiture.")
    async def buy(self, interaction: discord.Interaction, car_id: str):
        users = self.load_users()
        cars = self.load_cars()
        uid = str(interaction.user.id)

        if uid not in users:
            await interaction.response.send_message("Utilise /start d’abord.")
            return

        if car_id not in cars:
            await interaction.response.send_message("Voiture introuvable.")
            return

        price = cars[car_id]["price"]

        if users[uid]["money"] < price:
            await interaction.response.send_message("Tu n'as pas assez de crédits.")
            return

        users[uid]["money"] -= price
        users[uid]["garage"].append(car_id)
        self.save_users(users)

        await interaction.response.send_message(f"Tu as acheté **{cars[car_id]['name']}** !")


async def setup(bot):
    await bot.add_cog(Shop(bot))
