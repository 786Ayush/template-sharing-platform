import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "template_sharing_db")

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    if db.database is None:
        await connect_to_mongo()
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(
        MONGODB_URL,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=20000
    )
    db.database = db.client[DATABASE_NAME]
    print("Connected to MongoDB!")

async def close_mongo_connection():
    """Close database connection"""
    db.client.close()
    print("Disconnected from MongoDB!")

# Image storage logic
async def store_image_in_mongo(image_bytes: bytes, filename: str, content_type: str = "image/png"):
    """
    Store image in MongoDB 'images' collection.
    Args:
        image_bytes: Raw image data.
        filename: Name of the image file.
        content_type: MIME type of the image.
    Returns:
        Inserted document ID.
    """
    db_instance = await get_database()
    image_doc = {
        "filename": filename,
        "content_type": content_type,
        "data": image_bytes
    }
    result = await db_instance["images"].insert_one(image_doc)
    return result.inserted_id
