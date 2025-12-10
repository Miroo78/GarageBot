import discord
from discord.ext import commands
from discord import app_commands
import json, random

class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_auction(self):
        with open("data/auction.json", "r") as f:
            return json.load(f)

    def save_auction(self, data):
        with open("data/auction.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_cars(self):
        with open("data/cars.json", "r") as f:
            return json.load(f)

    def load_users(self):
        with open("data/users.json", "r") as f:
            return json.load(f)

    def save_users(self, data):
        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

    @app_commands.command(name="auction", description="Lancer une enchère.")
    async def auction(self, interaction: discord.Interaction):
        auction = self.load_auction()
        cars = self.load_cars()

        if auction["active"]:
            await interaction.response.send_message("Une enchère est déjà en cours.")
            return

        car_id = random.choice(list(cars.keys()))
        car = cars[car_id]

        start_price = int(car["price"] * 0.6)
        max_price = int(car["price"] * random.uniform(1.0, 1.8))

        auction["active"] = True
        auction["car_id"] = car_id
        auction["current_price"] = start_price
        auction["max_price"] = max_price

        self.save_auction(auction)

        await interaction.response.send_message(
            f"**Enchère lancée !**\nVoiture : {car['name']}\nPrix actuel : {start_price} crédits"
        )

    @app_commands.command(name="bid", description="Faire une offre à l'enchère.")
    async def bid(self, interaction: discord.Interaction, montant: int):
        auction = self.load_auction()
        users = self.load_users()
        cars = self.load_cars()
        uid = str(interaction.user.id)

        if not auction["active"]:
            await interaction.response.send_message("Aucune enchère en cours.")
            return

        if uid not in users:
            await interaction.response.send_message("Utilise /start d’abord.")
            return

        if users[uid]["money"] < montant:
            await interaction.response.send_message("Tu n'as pas assez d'argent.")
            return

        car_id = auction["car_id"]
        car = cars[car_id]

        # Simulation des acheteurs fantômes
        if montant < auction["max_price"]:
            new_price = montant + random.randint(100, 500)
            auction["current_price"] = new_price
            self.save_auction(auction)

            await interaction.response.send_message(
                f"Quelqu'un a surenchéri ! Nouveau prix : {new_price} crédits."
            )
            return

        # L'utilisateur gagne
        auction["active"] = False
        users[uid]["money"] -= auction["current_price"]
        users[uid]["garage"].append(car_id)

        self.save_users(users)
        self.save_auction({
            "active": False,
            "car_id": None,
            "current_price": 0,
            "max_price": 0
        })

        await interaction.response.send_message(
            f"🎉 Tu as **gagné l'enchère** ! Tu remportes **{car['name']}**."
        )


async def setup(bot):
    await bot.add_cog(Auction(bot))
