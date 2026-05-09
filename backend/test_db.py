from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("Database connected successfully!")
    connection.close()
except Exception as e:
    print(e)