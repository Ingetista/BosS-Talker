import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from threading import Thread
from flask import Flask
from database.connection import init_db # Importamos la función de inicialización de nuestra capa de datos

# Creo una mini aplicación Flask para mantener el bot activo en Render
app = Flask(' ')

@app.route('/')
def home():
    return "BosS-Talker está activo 24/7 y patrullando Discord."

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
def keep_alive():   # Arranca el servidor con un hilo secundario
    t = Thread(target=run_flask)
    t.start()


# Cargamos las variables de entorno del archivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 1. Configuración estricta de Intents (Permisos de la API de Discord)
class BossTalker(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Requerido para leer canales de texto y resumir
        intents.presences = True        # Requerido para rastrear el estado del jefe (Online/Offline)
        intents.members = True          # Requerido para mapear la lista de usuarios del servidor
        
        # Inicializamos el bot con un prefijo tradicional
        super().__init__(command_prefix="b!", intents=intents, help_command=None)

    # Este método se ejecuta automáticamente ANTES de que el bot se conecte a Discord.
    # Es el lugar ideal para preparar la infraestructura.
    
    # A. Inicializamos la base de datos local
    async def setup_hook(self):
        await init_db()
        
        # B. Cargamos los Cogs (módulos) de manera dinámica
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

    # Se ejecuta cuando el bot se conecta exitosamente a los servidores de Discord.
    async def on_ready(self):
        print("--------------------------------------------------")
        print(f"🤖 ¡BosS-Talker está en línea y patrullando!")
        print(f"Logueado como: {self.user.name} (ID: {self.user.id})")
        print("--------------------------------------------------")
        
        # SYNC LOCAL: (PRUEBA TEMPORAL)
        # ID de tu servidor de pruebas para forzar la sincronización inmediata
        GUILD_ID = discord.Object(id=1093346814691922030) # <-- PEGA TU ID AQUÍ (sin comillas, solo el número)
        
        try:
            # Copiamos los comandos globales al árbol de este servidor específico
            self.tree.copy_global_to(guild=GUILD_ID)
            # Sincronizamos localmente
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f"✨ [Slash Commands] {len(synced)} comandos sincronizados LOCALMENTE en el servidor de pruebas.")
        except Exception as e:
            print(f"❌ [Error] Falló la sincronización local: {e}")
            
        await self.change_presence(activity=discord.Game(name="Vigilando al patrón 👀"))
        
        
        
        
        """ SYNC GLOBAL       # Sincronizamos los comandos de barra diagonal (Slash Commands) globalmente
        try:
            synced = await self.tree.sync()
            print(f"✨ [Slash Commands] {len(synced)} comandos sincronizados globalmente.")
        except Exception as e:
            print(f"❌ [Error] Falló la sincronización de comandos: {e}")
            
        # Seteamos un estado divertido y criollo para el bot
        await self.change_presence(activity=discord.Game(name="Vigilando al patrón 👀"))
        """


# Función principal para arrancar el script asíncronamente
async def main():
    if not TOKEN:
        print("❌ [Error Crítico] No se encontró el DISCORD_TOKEN en el archivo .env")
        return
        
    bot = BossTalker()
    
    # Context manager para asegurar el cierre limpio de recursos
    async with bot:
        keep_alive()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())