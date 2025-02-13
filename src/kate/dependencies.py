"""Dependencies for the web application."""

# %% IMPORTS

import os
import typing as T

import aiohttp
import fastapi
from pipecat.transports.services.helpers import daily_rest

# %% TYPES

DailyRoom: T.TypeAlias = daily_rest.DailyRoomObject
DailyHelper: T.TypeAlias = daily_rest.DailyRESTHelper


class DailyConnection(T.TypedDict):
    """Connection to a daily room."""

    token: str
    room_url: str


# %% CONFIGS

DAILY_API_KEY = os.getenv("DAILY_API_KEY", None)

# %% DEPENDENCIES


async def get_daily_helper() -> T.AsyncGenerator[DailyHelper, None]:
    """Yield an instance of the Daily REST helper for dependency."""
    async with aiohttp.ClientSession() as aiohttp_session:
        yield DailyHelper(
            daily_api_key=DAILY_API_KEY,
            aiohttp_session=aiohttp_session,
        )


DailyHelperDependency: T.TypeAlias = T.Annotated[DailyHelper, fastapi.Depends(get_daily_helper)]
