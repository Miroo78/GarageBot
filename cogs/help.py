import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche la liste complète des commandes du bot.")
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📖 | Guide du Bot Collection Automobile",
            description="Voici toutes les commandes disponibles et leur utilité.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="💰 **Économie**",
            value=(
                "**/balance** — Affiche tes crédits\n"
                "**/daily** — Récompense quotidienne\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🏎️ **Garage**",
            value=(
                "**/garage** — Affiche ta collection de voitures\n"
                "**/carinfo** — Infos détaillées d’une voiture (si tu veux l'ajouter plus tard)\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🔨 **Enchères**",
            value=(
                "**/auction** — Lance une nouvelle enchère (voiture aléatoire)\n"
                "**/bid montant** — Propose une offre et affronte les acheteurs fantômes\n"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ **Utilitaires**",
            value=(
                "**/help** — Affiche ce menu\n"
                "**/ping** — Vérifie si le bot est en ligne\n"
            ),
            inline=False
        )

        embed.set_footer(text="Bot Automobile • Système d’enchères et de collection")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
