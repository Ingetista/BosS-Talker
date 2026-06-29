import aiosqlite
import os

# Definimos la ruta de la base de datos en la raíz del proyecto para local
DB_PATH = "boss_talker.db"

async def get_db_connection():
    """
    Retorna la conexión correcta a la base de datos.
    Si está en Render, la monta en la memoria RAM (:memory:).
    Si está en local, usa el archivo físico en la raíz.
    """
    # Render inyecta automáticamente la variable de entorno RENDER=true
    if os.getenv("RENDER"):
        print("☁️ [Database] Detectado entorno Render. Conectando a la memoria RAM (:memory:)...")
        return await aiosqlite.connect(":memory:")
    
    return await aiosqlite.connect(DB_PATH)

async def init_db():
    """
    Inicializa la base de datos local y crea las tablas necesarias
    si no existen en el sistema.
    """
    # Usamos la función inteligente para obtener la conexión adecuada
    async with await get_db_connection() as db:
        
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
        
        # Guardamos los cambios
        await db.commit()
        
    print("💾 [Database] Base de datos inicializada y tablas verificadas/creadas.")