import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv("TOKEN")
    DB_CONFIG = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
    }

    @classmethod
    def validate(cls):
        if not cls.TOKEN:
            raise ValueError("Токен не найден!")
        if not all(cls.DB_CONFIG.values()):
            raise ValueError("Не все параметры БД заданы!")