import os 
from dotenv import load_dotenv


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
account_name = os.getenv("ACCOUNT_NAME")
account_key = os.getenv("ACCOUNT_KEY" )
container_name = os.getenv("CONTAINER_NAME")



connection_string= os.getenv("CONNECTION_STRING")
