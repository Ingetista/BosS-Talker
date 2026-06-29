import aiosqlite
from database.connection import get_db_path

# Guarda o actualiza el canal asignado para las alertas de BosS-Talker
async def set_server_channel(guild_id: str, channel_id: str):
    async with aiosqlite.connect(get_db_path()) as db:
        await db.execute("""
            INSERT INTO server_config (guild_id, alert_channel_id)
            VALUES (?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET alert_channel_id = excluded.alert_channel_id
        """, (str(guild_id), str(channel_id)))
        await db.commit()

# Obtiene el ID del canal de alertas asignado a un servidor
async def get_server_channel(guild_id: str) -> str:
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.execute(
            "SELECT alert_channel_id FROM server_config WHERE guild_id = ?", 
            (str(guild_id),)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

# Registra a un usuario en la lista de vigilancia de un servidor específico
async def add_tracked_user(guild_id: str, user_id: str) -> bool:
    try:
        async with aiosqlite.connect(get_db_path()) as db:
            await db.execute(
                "INSERT INTO tracked_users (guild_id, user_id) VALUES (?, ?)",
                (str(guild_id), str(user_id))
            )
            await db.commit()
            return True
    except aiosqlite.IntegrityError:
        return False  # El usuario ya estaba siendo vigilado en este servidor

# Elimina a un usuario de la lista de vigilancia del servidor
async def remove_tracked_user(guild_id: str, user_id: str) -> bool:
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.execute(
            "DELETE FROM tracked_users WHERE guild_id = ? AND user_id = ?",
            (str(guild_id), str(user_id))
        ) as cursor:
            await db.commit()
            return cursor.rowcount > 0  # True si borró a alguien, False si no existía

# Verifica si un usuario específico está bajo seguimiento en ese servidor
async def is_user_tracked(guild_id: str, user_id: str) -> bool:
    async with aiosqlite.connect(get_db_path()) as db:
        async with db.execute(
            "SELECT 1 FROM tracked_users WHERE guild_id = ? AND user_id = ?",
            (str(guild_id), str(user_id))
        ) as cursor:
            row = await cursor.fetchone()
            return row is not None