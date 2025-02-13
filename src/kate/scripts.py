"""Command-line scripts for the project."""

# %% IMPORTS

import os
import signal
import sys

import uvicorn
from loguru import logger

# %% CONFIGS

KATE_DEV_MODE = bool(os.getenv("KATE_DEV_MODE", False))
KATE_SERVER_HOST = os.getenv("KATE_SERVER_HOST", "0.0.0.0")
KATE_SERVER_PORT = int(os.getenv("KATE_SERVER_PORT", "8080"))

# %% HANDLERS


def exit_handler(signal, frame) -> None:
    """Handle signals to exit program."""
    logger.info(f"Exit Handler: signal={signal}")
    sys.exit(0)


# %% SCRIPTS


def main(argv: list[str] | None = None) -> None:
    """Execute the main script of the project."""
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)
    uvicorn.run(
        app="kate.servers:app",
        host=KATE_SERVER_HOST,
        port=KATE_SERVER_PORT,
        reload=KATE_DEV_MODE,
        timeout_graceful_shutdown=0,
    )
