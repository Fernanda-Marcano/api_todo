from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = 'mongodb://localhost:27017'
client = AsyncIOMotorClient(MONGO_URI)
database = client['todo']
collection = database['task']