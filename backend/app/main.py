from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.api.main import api_router
from fastapi import FastAPI

description = """
Changelog API helps you manage your changelogs.

## Product

- You have standard **crud** to manage your products.
- You can get paginated updates for your product in ascending order.

## Update

- You get standard **crud** to manage your updates.
- You get updates for your product filtered by update status (_not implemented_).

## Update-points

- You get standard **crud** to manage points of your update.
- You get update points for update filtered by type(_not implemented_).

## Users

You will be able to:
* **signin** (_basic implementation_)
* **Create users** (_basic implementation_)
* **Read users** (_not implemented_).
"""


# models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(
    title="Changelog API",
    description=description,
    contact={
        "name": "Marcin",
        "email": "mn.wlodarczyk@gmail.com",
    },
    license_info={"name": "Beerware License"},
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
