import psycopg2
from psycopg2.extras import Json
from config import settings

class Database:
    def __init__(self):
        self.conn_string = settings.DB_CONNECTION

    def verify_tables(self):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
                return [table[0] for table in cur.fetchall()]

    def setup(self):
        """Create initial database tables"""
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS processed_emails (
                        id SERIAL PRIMARY KEY,
                        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        raw_content TEXT,
                        extracted_info JSONB,
                        model_used VARCHAR(50),
                        processing_time FLOAT,
                        status VARCHAR(20)
                    )
                """)

                cur.execute("""
                   CREATE TABLE IF NOT EXISTS email_accounts (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255),
                    password VARCHAR(255),
                    imap_server VARCHAR(255),
                    active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
           """)
                conn.commit()
    def get_active_accounts(self):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM email_accounts WHERE active = true")
                return cur.fetchall()
            
    def add_email_account(self, email: str, password: str, imap_server: str):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO email_accounts (email, password, imap_server)
                    VALUES (%s, %s, %s)
                    RETURNING id
           """, (email, password, imap_server))
                return cur.fetchone()[0]

    def save_email(self, raw_content: str, extracted_info: dict, 
                  model_used: str, processing_time: float):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO processed_emails 
                    (raw_content, extracted_info, model_used, processing_time, status)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (raw_content, Json(extracted_info), model_used, 
                     processing_time, 'completed'))
                return cur.fetchone()[0]

    def get_email(self, email_id: int):
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM processed_emails WHERE id = %s
                """, (email_id,))
                return cur.fetchone()