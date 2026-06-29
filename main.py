import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from threading import Thread
from flask import Flask
from database.connection import init_db

# 1. Configuración limpia de Flask (Keep-Alive para Render)
app = Flask(' ')

@app.route('/')
def home():
    return "BosS-Talker está activo 24/7 y patrullando Discord. 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    # use_reloader=False evita que Flask intente duplicar el proceso en la nube
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    
def keep_alive():   
    # daemon=True asegura que corra de fondo sin congelar a Discord
    t = Thread(target=run_flask, daemon=True)
    t.start()
    print("🌐 [Keep-Alive] Servidor web espejo iniciado de fondo.")

# Cargamos las variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2. Configuración estricta de la clase BossTalker
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
    if not TOKEN:
        print("❌ [Error Crítico] No se encontró el DISCORD_TOKEN en las variables de entorno.")
        return
        
    bot = BossTalker()
    
    async with bot:
        # Lanzamos el servidor de supervivencia en su hilo demonio
        keep_alive()
        # Encendemos el bot de Discord
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Bot apagado.")