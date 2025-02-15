"""Cleaning tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS

# %% - Tools


@task
def mypy(ctx: Context) -> None:
    """Clean the mypy tool."""
    ctx.run("rm -rf .mypy_cache/")


@task
def ruff(ctx: Context) -> None:
    """Clean the ruff tool."""
    ctx.run("rm -rf .ruff_cache/")


@task
def pytest(ctx: Context) -> None:
    """Clean the pytest tool."""
    ctx.run("rm -rf .pytest_cache/")


@task
def coverage(ctx: Context) -> None:
    """Clean the coverage tool."""
    ctx.run("rm -f .coverage*")


# %% - Folders


@task
def dist(ctx: Context) -> None:
    """Clean the dist folder."""
    ctx.run("rm -f dist/*")


@task
def docs(ctx: Context) -> None:
    """Clean the docs folder."""
    ctx.run("rm -rf docs/*")


@task
def cache(ctx: Context) -> None:
    """Clean the cache folder."""
    ctx.run("rm -rf .cache/")


# %% - Sources


@task
def venv(ctx: Context) -> None:
    """Clean the venv folder."""
    ctx.run("rm -rf .venv/")


@task
def uv(ctx: Context) -> None:
    """Clean uv lock file."""
    ctx.run("rm -f uv.lock")


@task
def node(ctx: Context) -> None:
    """Clean the node_modules folder."""
    ctx.run("rm -rf client/node_modules/")


@task
def python(ctx: Context) -> None:
    """Clean python caches and bytecodes."""
    ctx.run("find . -type f -name '*.py[co]' -delete")
    ctx.run(r"find . -type d -name __pycache__ -exec rm -r {} \+")


# %% - Combines


@task(pre=[mypy, ruff, pytest, coverage])
def tools(_: Context) -> None:
    """Run all tools tasks."""


@task(pre=[dist, docs, cache])
def folders(_: Context) -> None:
    """Run all folders tasks."""


@task(pre=[venv, uv, node, python])
def sources(_: Context) -> None:
    """Run all sources tasks."""


@task(pre=[tools, folders], default=True)
def all(_: Context) -> None:
    """Run all tools and folders tasks."""


@task(pre=[all, sources])
def reset(_: Context) -> None:
    """Run all tools, folders and sources tasks."""
