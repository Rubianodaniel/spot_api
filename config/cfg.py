import os 
from dotenv import load_dotenv


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
account_name = os.getenv("ACCOUNT_NAME")
account_key = os.getenv("ACCOUNT_KEY" )
container_name = os.getenv("CONTAINER_NAME")



conecction_string= os.getenv("CONNECTION_STRING")
# conecction_string = (f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net")
