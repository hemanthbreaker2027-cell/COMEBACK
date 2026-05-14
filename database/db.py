from motor.motor_asyncio import AsyncIOMotorClient
from config.config import Config
import os

class Database:
    def __init__(self):
        uri = Config.MONGO_URI or "mongodb://localhost:27017"
        if os.getenv("TESTING") == "1":
            from mongomock_motor import AsyncMongoMockClient as MockClient
            self.client = MockClient()
        else:
            self.client = AsyncIOMotorClient(uri)
        self.db = self.client[Config.DB_NAME]
        self.anime = self.db.anime
        self.users = self.db.users
        self.settings = self.db.settings

    async def add_anime(self, data):
        return await self.anime.update_one({"mal_id": data["mal_id"]}, {"$set": data}, upsert=True)

    async def get_anime_by_mal_id(self, mal_id):
        return await self.anime.find_one({"mal_id": mal_id})

    async def get_anime_by_slug(self, slug):
        return await self.anime.find_one({"slug": slug})

    async def get_all_anime(self, limit=20, skip=0):
        return await self.anime.find().sort("_id", -1).skip(skip).limit(limit).to_list(length=limit)

    async def search_anime_db(self, query):
        return await self.anime.find({"title": {"$regex": query, "$options": "i"}}).to_list(length=20)

    async def delete_anime(self, mal_id):
        return await self.anime.delete_one({"mal_id": mal_id})

    async def update_settings(self, key, value):
        await self.settings.update_one({"key": key}, {"$set": {"value": value}}, upsert=True)

    async def get_settings(self, key):
        res = await self.settings.find_one({"key": key})
        return res["value"] if res else None

db = Database()
