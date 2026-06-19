import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando de barra diagonal de prueba (/ping)
    @app_commands.command(name="ping", description="Verifica la latencia de BosS-Talker")
    async def ping(self, interaction: discord.Interaction):
        latencia = round(self.bot.latency * 1000)
        # Respuesta criolla y amigable
        await interaction.response.send_message(
            f"¡Habla, mano! Estoy fino. 🚀 Latencia: **{latencia}ms**. Civilízate."
        )

async def setup(bot):
    await bot.add_cog(General(bot))