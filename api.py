from dotenv import load_dotenv
import os 

load_dotenv()

env = os.getenv("ENV")
api_address = os.getenv(f"{env}_API_ADDRESS")

shopping_list_api_endpoints = f'http://{api_address}:8000/recipe/get_shopping_list'
database_api_endpoints = f'http://{api_address}:8000/database/'