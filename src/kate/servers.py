"""Handle HTTP requests and manage bots."""

# %% IMPORTS

import asyncio
import os
import typing as T

import fastapi
from fastapi.middleware import cors
from fastapi.staticfiles import StaticFiles
from loguru import logger
from pipecat.transports.services.helpers import daily_rest

from kate import bots, dependencies

# %% TYPES


class DailyConnection(T.TypedDict):
    """Connection to a daily room."""

    token: str
    room_url: str


# %% ASSETS

STATIC_FILES = os.path.join(os.path.dirname(__file__), "clients")

# %% CONFIGS

DAILY_ROOM_NAME = os.getenv("DAILY_ROOM_NAME", None)
KATE_BOT_NAME = os.getenv("KATE_BOT_NAME", "OTLBot")
KATE_DEV_MODE = bool(os.getenv("KATE_DEV_MODE", False))
KATE_SERVER_URL = os.getenv("KATE_SERVER_URL", None)

# %% ASSERTIONS

assert KATE_BOT_NAME.endswith("Bot"), f"KATE_BOT_NAME must end with 'Bot': {KATE_BOT_NAME}"

# %% APPLICATIONS

# Initialize a FastAPI application
app = fastapi.FastAPI(title="Kate")
# Configure CORS to allow requests
app.add_middleware(
    cors.CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=[KATE_SERVER_URL],
    allow_credentials=True,
)
# Mount the client static files
app.mount(
    path="/app",
    name="client",
    app=StaticFiles(directory=STATIC_FILES, html=True),
)

# %% OPERATIONS


@app.get("/")
async def index() -> fastapi.responses.RedirectResponse:
    """Redirect the user to the client application."""
    return fastapi.responses.RedirectResponse("/app")


@app.post("/connect")
async def rtvi_connect(
    request: fastapi.Request, daily_helper: dependencies.DailyHelperDependency
) -> dependencies.DailyConnection:
    """Connect operation that creates a bot and returns connection credentials."""
    if DAILY_ROOM_NAME is not None and KATE_DEV_MODE:
        logger.info(f"Delete existing Daily room: {DAILY_ROOM_NAME}")
        success = await daily_helper.delete_room_by_name(room_name=DAILY_ROOM_NAME)
        logger.info(f"Deleting existing Daily room {DAILY_ROOM_NAME}: success={success}")
    logger.info(f"Create new Daily room for RTVI connection: {DAILY_ROOM_NAME}")
    params = daily_rest.DailyRoomParams(name=DAILY_ROOM_NAME, privacy="private")
    room = await daily_helper.create_room(params=params)
    logger.info(f"Created Daily room: {room}")
    if not room.url:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to create Daily room: {params}"
        )
    token = await daily_helper.get_token(room_url=room.url, owner=True)
    if not token:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to get token for Daily room: {room.url}"
        )
    try:
        BotClass = getattr(bots, KATE_BOT_NAME)
        bot = BotClass(room_url=room.url, token=token)
        task = asyncio.create_task(bot.run(), name=room.url)
        logger.info(f"Bot task name created: {task.get_name()}")
    except Exception as error:
        raise fastapi.HTTPException(status_code=500, detail=f"Failed to start bot: {error}")
    return DailyConnection(room_url=room.url, token=token)
