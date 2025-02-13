"""Spider tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def otl(ctx: Context) -> None:
    """Scrape Open Textbook Library dataset."""
    with ctx.cd("spiders"):
        ctx.run("uv run python otl.py")


@task(pre=[otl], default=True)
def all(_: Context) -> None:
    """Run all spider tasks."""
