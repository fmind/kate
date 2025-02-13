"""Package tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

from . import cleans

# %% TASKS


@task(pre=[cleans.dist])
def build(ctx: Context) -> None:
    """Build the python package."""
    ctx.run("uv build --wheel")


@task
def requirements(ctx: Context) -> None:
    """Generate a requirements.txt"""
    ctx.run(
        "uv export --format=requirements-txt --no-dev "
        "--no-hashes --no-editable --no-emit-project "
        "--output-file=requirements.txt"
    )


@task(pre=[build, requirements], default=True)
def all(_: Context) -> None:
    """Run all package tasks."""
