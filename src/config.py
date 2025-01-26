import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_CONNECTION = os.getenv("DB_CONNECTION", "postgresql://mitalijuvekar@localhost:5432/email_processor")
    
    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

settings = Settings()