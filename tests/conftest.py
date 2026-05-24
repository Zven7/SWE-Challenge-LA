import asyncio
import os
import sys

import pytest
from fastapi.testclient import TestClient
import mongomock
from mongomock_motor import AsyncMongoMockClient

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

from app.db.models.user import User
from app.main import app
import app.db.client as db_client
from app.core.config import settings


@pytest.fixture(autouse=True)
def test_db(monkeypatch):
    monkeypatch.setattr(db_client, "AsyncIOMotorClient", AsyncMongoMockClient)
    monkeypatch.setattr(settings, "mongodb_url", "mongodb://localhost:27017")
    monkeypatch.setattr(settings, "mongodb_db_name", "test_db")

    orig_list_collection_names = mongomock.database.Database.list_collection_names

    def safe_list_collection_names(self, *args, **kwargs):
        kwargs.pop("authorizedCollections", None)
        kwargs.pop("nameOnly", None)
        return orig_list_collection_names(self, *args, **kwargs)

    monkeypatch.setattr(
        mongomock.database.Database,
        "list_collection_names",
        safe_list_collection_names,
    )

    db_client.client = None

    yield

    if db_client.client:
        asyncio.run(db_client.close_db())
    try:
        asyncio.run(User.find_all().delete())
    except Exception:
        pass


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
