from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.db.models.user import User

client: AsyncIOMotorClient | None = None


async def init_db():
    global client

    client = AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User],
    )


async def close_db():
    global client
    if client:
        client.close()
        client = None