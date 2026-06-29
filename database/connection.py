import aiosqlite
import os

# Definimos la ruta de la base de datos física para tu PC local
DB_PATH = "boss_talker.db"

def get_db_path():
    """
    Retorna el string de conexión correcto según el entorno.
    """
    if os.getenv("RENDER"):
        print("☁️ [Database] Detectado entorno Render. Apuntando a la memoria RAM (:memory:)...")
        return ":memory:"
    return DB_PATH

async def init_db():
    """
    Inicializa la base de datos local y crea las tablas necesarias.
    """
    # Obtenemos la ruta correcta directamente sin crear conexiones intermedias rotas
    path = get_db_path()
    
    # La sintaxis correcta y limpia de aiosqlite es simplemente 'async with aiosqlite.connect(...)'
    async with aiosqlite.connect(path) as db:
        
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
        
        # Guardamos los cambios
        await db.commit()
        
    print("💾 [Database] Base de datos inicializada y tablas verificadas/creadas con éxito.")