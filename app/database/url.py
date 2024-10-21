from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the MONGO_URI from the environment variables
MONGO_URI = os.getenv('MONGO_URI')
