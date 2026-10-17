from dotenv import load_dotenv
import os
load_dotenv()
DB_KEY = os.getenv("PG_URL")
API_KEY = os.getenv("API_KEY")

if DB_KEY is None:
    raise RuntimeError("DB_KEY is not set in .env")
if API_KEY is None:
    raise RuntimeError("API_KEY is not set in .env")