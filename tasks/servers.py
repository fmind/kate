"""Server tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def run(ctx: Context, mode: str = "development") -> None:
    """Run the project server."""
    ctx.run(f"UV_ENV_FILE=.env.{mode} uv run kate")


@task(pre=[run], default=True)
def all(_: Context) -> None:
    """Run all server tasks."""
