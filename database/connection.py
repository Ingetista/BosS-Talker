import aiosqlite
import os

# Definimos la ruta de la base de datos en la raíz del proyecto
DB_PATH = "boss_talker.db"

async def init_db():
    
    """
    Inicializa la base de datos local y crea las tablas necesarias
    si no existen en el sistema.
    
    """
    async with aiosqlite.connect(DB_PATH) as db:
        
        # 1. Tabla para configurar el canal de alertas de cada servidor de Discord
        await db.execute("""
            CREATE TABLE IF NOT EXISTS server_config (
                guild_id TEXT PRIMARY KEY,
                alert_channel_id TEXT NOT NULL
            )
        """)
        
        # 2. Tabla para almacenar los usuarios que se van a monitorear por servidor
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tracked_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                UNIQUE(guild_id, user_id),
                FOREIGN KEY (guild_id) REFERENCES server_config(guild_id) ON DELETE CASCADE
            )
        """)
        
        """
        DETALLITO: Implementé TEXT para guardar los IDs de Discord como strings, 
        ya que pueden ser números muy grandes y podrían generar desbordamiento de Bits.
        
        """
        
        # Guardamos los cambios en el archivo físico
        await db.commit()
    print("💾 [Database] Base de datos inicializada y tablas verificadas/creadas.")