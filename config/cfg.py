import os 
from dotenv import load_dotenv


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
connection_string= os.getenv("CONNECTION_STRING")
