import psycopg
from pgvector.psycopg import register_vector
from .config import Config

class Database:
    def __init__(self):
        self.url = Config.DATABASE_URL

    def connect(self):
        conn = psycopg.connect(self.url)
        register_vector(conn)
        return conn

    def init_schema(self):
        CREATE_DOCUMENTS = """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            source_type TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """

        CREATE_CHUNKS = f"""
        CREATE TABLE IF NOT EXISTS chunks (
            id SERIAL PRIMARY KEY,
            document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding VECTOR(960),
            token_count INTEGER,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """

        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(CREATE_DOCUMENTS)
            cur.execute(CREATE_CHUNKS)
        conn.commit()
        conn.close()

    def get_embedding_dimension(self):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT atttypmod - 4
                FROM pg_attribute
                WHERE attrelid = 'chunks'::regclass
                AND attname = 'embedding';
            """)
            dim = cur.fetchone()[0]
        conn.close()
        return dim
