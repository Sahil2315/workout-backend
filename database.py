from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

# Load MongoDB URL from environment
MONGO_URL = os.getenv("MONGO_URL")

# Create client and database reference
client = AsyncIOMotorClient(MONGO_URL)
db = client["plankoutDB"]  # Replace with your actual DB name

# Optional: define collections here for reuse
user_collection = db["users"]
product_collection = db["workouts"]
