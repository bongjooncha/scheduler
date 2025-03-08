from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import MONGODB_URL, DATABASE_NAME, COLLECTION_NAME

client = None
db = None
collection = None

async def connect_to_mongo():
    global client, db, collection
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

async def close_mongo_connection():
    global client
    if client:
        client.close() 