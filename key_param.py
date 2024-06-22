import os
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

database_url = os.getenv("DATABASE_URL")
