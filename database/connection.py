import aiosqlite
import os

# Definimos la ruta de la base de datos física
DB_PATH = "boss_talker.db"

def get_db_path():
    """
    Retorna siempre el archivo físico para mantener la persistencia
    entre las diferentes consultas de los comandos.
    """
    return DB_PATH

async def init_db():
    """
    Inicializa la base de datos local y crea las tablas necesarias.
    """
    async with aiosqlite.connect(get_db_path()) as db:
        
        # 1. Tabla para configurar el canal de alertas
        await db.execute("""
            CREATE TABLE IF NOT EXISTS server_config (
                guild_id TEXT PRIMARY KEY,
                alert_channel_id TEXT NOT NULL
            )
        """)
        
        # 2. Tabla para almacenar los usuarios que se van a monitorear
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tracked_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                UNIQUE(guild_id, user_id),
                FOREIGN KEY (guild_id) REFERENCES server_config(guild_id) ON DELETE CASCADE
            )
        """)
        
        await db.commit()
        
    print("💾 [Database] Base de datos física inicializada con éxito.")