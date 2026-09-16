import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database.connection import init_db

# Cargamos las variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configuración estricta de la clase BossTalker
class BossTalker(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Requerido para leer canales de texto y resumir
        intents.presences = True        # Requerido para rastrear el estado del jefe (Online/Offline)
        intents.members = True          # Requerido para mapear la lista de usuarios del servidor
        
        super().__init__(command_prefix="b!", intents=intents, help_command=None)

    # Inicializamos la base de datos y los Cogs antes de conectar
    async def setup_hook(self):
        await init_db()
        
        initial_extensions = [
            'cogs.general',
            'cogs.stalker',
            'cogs.summarizer'
        ]
        
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"📦 [Extension] '{extension}' cargada exitosamente.")
            except Exception as e:
                print(f"❌ [Error] No se pudo cargar la extensión {extension}. Motivo: {e}")

    # Se ejecuta cuando el bot se conecta exitosamente a Discord
    async def on_ready(self):
        print("--------------------------------------------------")
        print(f"🤖 ¡BosS-Talker está en línea y patrullando de forma GLOBAL!")
        print(f"Logueado como: {self.user.name} (ID: {self.user.id})")
        print("--------------------------------------------------")
        
        # SINCRONIZACIÓN GLOBAL DEFINITIVA (Modo Producción)
        try:
            synced = await self.tree.sync()
            print(f"✨ [Slash Commands] {len(synced)} comandos sincronizados GLOBALMENTE en todos los servidores.")
        except Exception as e:
            print(f"❌ [Error] Falló la sincronización global de comandos: {e}")
            
        await self.change_presence(activity=discord.Game(name="Vigilando al patrón 👀"))

# Función principal para arrancar el script asíncronamente
async def main():
    
    discord.utils.setup_logging() # Encendí los logs de discord para encontrar errores
    
    if not TOKEN:
        print("❌ [Error Crítico] No se encontró el DISCORD_TOKEN en las variables de entorno.")
        return
        
    bot = BossTalker()
    
    async with bot:
        # Encendemos el bot de Discord
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Bot apagado.")