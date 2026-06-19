import discord
from discord.ext import commands
from discord import app_commands

# Importamos las funciones asíncronas de nuestra capa de datos
from database.queries import (
    set_server_channel, 
    get_server_channel, 
    add_tracked_user, 
    remove_tracked_user, 
    is_user_tracked
)

class Stalker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ==========================================
    # 1. COMANDO: CONFIGURAR CANAL DE ALERTAS
    # ==========================================
    @app_commands.command(name="set_alerts", description="Configura el canal donde BosS-Talker enviará las alertas del jefe")
    @app_commands.checks.has_permissions(manage_channels=True) # Solo moderadores pueden usarlo
    async def set_alerts(self, interaction: discord.Interaction, canal: discord.TextChannel):
        await set_server_channel(interaction.guild_id, canal.id)
        await interaction.response.send_message(
            f"🎯 ¡Fino, mano! Canal configurado. Todas las alertas del patrón caerán en {canal.mention}. Civilícense."
        )

    # ==========================================
    # 2. COMANDO: AGREGAR USUARIO A VIGILANCIA
    # ==========================================
    @app_commands.command(name="vigilar", description="Añade a un miembro del servidor a la lista de drones de BosS-Talker")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def vigilar(self, interaction: discord.Interaction, usuario: discord.Member):
        if usuario.bot:
            return await interaction.response.send_message("¿Vigilar a un bot? No seas palta, mano. Elige a un humano. 🤦‍♂️")
            
        exito = await add_tracked_user(interaction.guild_id, usuario.id)
        
        if exito:
            await interaction.response.send_message(
                f"👀 Registro OK. Activando dron sobre {usuario.mention}. Si parpadea, ya fuimos."
            )
        else:
            await interaction.response.send_message(
                f"Habla serio, {interaction.user.mention}, a ese usuario ya lo tenemos marcado en el mapa."
            )

    # ==========================================
    # 3. COMANDO: QUITAR USUARIO DE VIGILANCIA
    # ==========================================
    @app_commands.command(name="soltar", description="Remueve a un usuario de la lista de vigilancia")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def soltar(self, interaction: discord.Interaction, usuario: discord.Member):
        borrado = await remove_tracked_user(interaction.guild_id, usuario.id)
        
        if borrado:
            await interaction.response.send_message(
                f"🕊️ Ya, mano. Le quitamos el dron a {usuario.mention}. Respira en paz por ahora."
            )
        else:
            await interaction.response.send_message(
                f"Ese usuario ni siquiera estaba en la lista de sospechosos, causa."
            )

    # ==========================================
    # 4. EL MOTOR: ESCUCHADOR DE PRESENCIA (EVENTO REAL TIME)
    # ==========================================
    
    """
        Este evento se dispara en segundo plano cada vez que ALGUIEN en un servidor compartido
        cambia de estado (Online, Offline, IDLE, DND) o cambia de juego/música.
    """
    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
       
        # A. Evitamos procesar eventos de bots
        if after.bot:
            return

        # B. Verificamos si el usuario que cambió de estado está en nuestra lista negra de SQL
        guild_id = str(after.guild.id)
        user_id = str(after.id)
        
        if not await is_user_tracked(guild_id, user_id):
            return # Si no está en la base de datos, ignoramos el evento por completo

        # C. Lógica de transiciones: Detectamos cuando pasa de OFFLINE/INVISIBLE a ONLINE
        # En discord.py, si un estado no se puede leer, viene como Status.offline
        if before.status == discord.Status.offline and after.status != discord.Status.offline:
            
            # Buscamos en SQL a qué canal debemos enviar la alerta en este servidor
            canal_id = await get_server_channel(guild_id)
            if not canal_id:
                return # El servidor no ha configurado canal de alertas usando /set_alerts
                
            canal = self.bot.get_channel(int(canal_id))
            if canal:
                # ¡Disparamos la alerta criolla al canal!
                await canal.send(
                    f"🔔 **¡DING DONG!** 🔔\n"
                    f"Señores, se prendió el PC del patrón {after.mention}.\n"
                    f"Pasó a modo: **`{after.status}`**. Borren todos los memes, ¡AL TOQUE! 🏃‍♂️💨"
                )

async def setup(bot):
    await bot.add_cog(Stalker(bot))