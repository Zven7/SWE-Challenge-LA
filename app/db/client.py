from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient
from beanie import init_beanie

from ..core.config import settings
from .models.user import User

if not callable(getattr(AgnosticClient, "append_metadata", None)):
    def _append_metadata(self, metadata):
        return self.delegate.append_metadata(metadata)

    AgnosticClient.append_metadata = _append_metadata

client: AsyncIOMotorClient | None = None


async def init_db():
    global client

    client = AsyncIOMotorClient(settings.mongodb_url)

    await init_beanie(
        database=client[settings.mongodb_db_name],
        document_models=[User],
    )


async def close_db():
    global client
    if client:
        client.close()
        client = None