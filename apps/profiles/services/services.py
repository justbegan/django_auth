from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_URL = os.environ.get('mongo_url')
MONGO_USER = os.environ.get('mongo_user')
MONGO_PASS = os.environ.get('mongo_pass')


def get_all_contest_from_fast_api() -> dict:
    client = MongoClient(
        MONGO_URL,
        username=MONGO_USER,
        password=MONGO_PASS
    )

    db = client["contest"]
    collection = db["contests"]
    obj = collection.find({})
    result = []
    for i in obj:
        i["_id"] = str(i["_id"])
        result.append(i)
    result = {item['_id']: item['title'] for item in result}
    return result


def get_contest_modules_by_contest_id(contest_id: str) -> list:
    client = MongoClient(
        MONGO_URL,
        username=MONGO_USER,
        password=MONGO_PASS
    )

    db = client["contest"]
    collection = db["contests"]
    obj = collection.find_one({"_id": ObjectId(contest_id)})
    try:
        result = obj["modules"]
        return result
    except:
        return None
