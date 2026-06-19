import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
# Importamos el nuevo cliente oficial de Google GenAI
from google import genai

class Summarizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # El nuevo SDK inicializa un cliente limpio buscando la variable GEMINI_API_KEY por defecto
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            # Inicializamos el cliente moderno
            self.client = genai.Client(api_key=gemini_key, http_options={'api_version': 'v1'})
            # En el nuevo SDK el string estándar actual es simplemente 'gemini-1.5-flash'
            self.model_name = 'gemini-2.5-flash'
        else:
            self.client = None
            print("❌ [Error] No se encontró GEMINI_API_KEY en las variables de entorno.")

    @app_commands.command(name="resumen", description="Genera un resumen express y criollo de lo conversado en este canal")
    @app_commands.describe(limite="Número de mensajes a leer para el resumen (máx 150)")
    async def resumen(self, interaction: discord.Interaction, limite: int = 50):
        if limite > 150:
            return await interaction.response.send_message("¡Bájele un toque! Máximo puedo leer 150 mensajes para no fundirme el cerebro. 😂")
        if limite < 5:
            return await interaction.response.send_message("No, cuchito. Pídame al menos 5 mensajes para poder chismosear bien.")

        await interaction.response.defer(thinking=True)

        if not self.client:
            return await interaction.followup.send("Lo siento, mi pana. Mi cerebro de IA no está configurado (falta la API Key).")

        # 1. Recolectar el historial de mensajes
        texto_historial = ""
        async for message in interaction.channel.history(limit=limite, oldest_first=False):
            if message.author.bot:
                continue
            texto_historial += f"[{message.author.name}]: {message.content}\n"

        if not texto_historial.strip():
            return await interaction.followup.send("Este canal está más vacío que billetera a fin de mes. No hay nada que resumir, mano. 💸")

        # 2. Diseñar el System Prompt criollo
        system_prompt = (
            "Actuando como 'BosS-Talker', un bot de Discord carismático, criollo y con mucho barrio colombiano, "
            "haz un resumen ejecutivo pero divertido del historial de chat que te proporcionaré.\n"
            "Sigue estas reglas estrictas:\n"
            "1. Entrega el resumen en máximo 3 o 4 bullets (puntos clave).\n"
            "2. Usa jerga colombiana moderada y natural (como 'paila', 'chimba', 'al toque', 'manito', 'cucho', 'parcero', 'civilízate', 'Sóbelo').\n"
            "3. Si detectas discusiones intensas, ponle el emoji 🔥 y di que 'se armó la trifulca' o 'hubo pelea'.\n"
            "4. Si hablaron de comida o salidas, ponle 🍔.\n"
            "5. Si el chat estuvo lleno de spam, ponle el emoji 💤 y califícalo con humor."
            "6. Si la conversación es un tema serio o ejecutivo, olvida todo lo anterior y haz un resumen formal sin jerga ni emojis, como si fueras un asistente ejecutivo de alta confianza."
        )

        # 3. Disparar la consulta al nuevo SDK de forma asíncrona
        try:
            # Usamos el nuevo método estructurado client.models.generate_content
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=f"{system_prompt}\n\nHistorial de chat:\n{texto_historial}"
            )
            resumen_final = response.text

            # 4. Enviar el resultado estilizado
            embed = discord.Embed(
                title="📝 Resumen Express de Barrio",
                description=resumen_final,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Analizados los últimos {limite} mensajes por orden del patrón.")
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"❌ Error al generar contenido con el nuevo SDK de Gemini: {e}")
            await interaction.followup.send("Asumadre, mano... Me dio un calambre cerebral con el nuevo satélite de Google. Intenta más tarde. 🧠⚡")

async def setup(bot):
    await bot.add_cog(Summarizer(bot))