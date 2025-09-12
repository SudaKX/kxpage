
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.v1 import (
    create_db_pool, close_db_pool, setup_routers, event_router, image_router,
    use_event_loop
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_pool()
    setup_routers()
    yield
    await close_db_pool()


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
app.include_router(event_router)
app.include_router(image_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    from uvicorn import Config, Server
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    use_event_loop(loop)
    config = Config(
        app, loop=loop, host="0.0.0.0", port=8000, log_level="info"
    )
    ser = Server(config=config)
    loop.run_until_complete(ser.serve())
    loop.close()
