from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from .config import Config
import pandas as pd


Base = declarative_base()

class Database:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def session(self):
        return self.SessionLocal()
    
    def check_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print("✗ Database connection FAILED")
            print("Error:", e)
            return False
        
    def show_schema(self):
        print("✓ DB Schema")
        for table_name, table in Base.metadata.tables.items():
            rows = []
            for column in table.columns:
                rows.append({
                    "column": column.name,
                    "type": str(column.type),
                    "primary_key": column.primary_key,
                    "nullable": column.nullable,
                    "default": column.default
                })

            df = pd.DataFrame(rows)
            print(f"\nTable: {table_name}")
            print(df.to_string(index=False))
    
    # Drop entire public schema    
    def set_new_environment(self):
        with self.engine.connect() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            conn.commit()
        print("✓ Schema reset")

        # Create pgvector extension
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()
        print("✓ pgvector extension ready")

        # Recreate tables
        Base.metadata.create_all(self.engine)   
