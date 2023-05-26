import motor
from config import *
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client['subscribeprivate']
USERS = db.users
TOKENS = db.tokens
ADMINS = db.admins

async def store_details(document):
    q = USERS.find_one({"user_id": document["user_id"]})
    if q:
        await USERS.delete_one({"user_id": document["user_id"]})
    q = await USERS.insert_one(document)
    if q.inserted_count == 1:
        return True