import motor, datetime
from config import *


client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

db = client['subscribeprivate']
USERS = db.users
TOKENS = db.tokens
ADMINS = db.admins
SENT_MESSAGES = db.sent_messages #To keep track of number of messages sent daily for users


async def store_details(document, existing_user):
    q = USERS.find_one({"user_id": document["user_id"]})
    q = await q.to_list(1)
    if not existing_user:
        document['active'] = 0 #Subscription is not yet active
    else:
        document['active'] = 1
    document['max_daily_notifications'] = 999
    if q:
        await USERS.delete_one({"user_id": document["user_id"]})
    q = await USERS.insert_one(document)
    if q.inserted_count == 1:
        return True

async def add_subscription(token, user_id):
    """
    Schema:
        "generated_on": <time>
        "expiry"      : <time>
        "used"        : 1/0
    """
    q = TOKENS.find({"token": token})
    q = await q.to_list(1)
    if q:
        if q[0]['used'] == 1:
            return "The token has already been used."
        now = datetime.datetime.now()
        token_expires_on = datetime.datetime.fromtimestamp(q[0]['expiry'])
        if now > token_expires_on:
            return "The token has expired."
        q = await TOKENS.update_one({"token": token}, {"$set": {"used": 1}})
        if q.modified_count == 1:
            await USERS.update_one({"user_id": user_id}, {"$set": {"active": 1}})
            return "You have successfully subscribed."
        else:
            return "Something went wrong, try again. /start"
        
async def remove_subscription(user_id):
    await USERS.update_one({"user_id": user_id}, {"$set": {"active": 0}})

async def user_is_active(user_id):
    q = USERS.find({"user_id": user_id, "active": 1})
    q = await q.to_list(1)
    if q:
        return True

async def update_notif_preferences(user_id, num):
    await USERS.update_many({"user_id": user_id}, {"$set": {"max_daily_notifications": int(num)}})

async def get_all_admins():
    admins = ADMINS.find({})
    admins = await admins.to_list(999)
    return admins