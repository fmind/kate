"""Container tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

from . import clients, packages

# %% CONFIGS

IMAGE_TAG = "latest"

# %% TASKS


@task
def compose(ctx: Context) -> None:
    """Start up docker compose."""
    ctx.run("docker compose up")


@task(pre=[clients.build, packages.build])
def build(ctx: Context, tag: str = IMAGE_TAG) -> None:
    """Build the container image."""
    ctx.run(f"docker build --tag={ctx.project.repository}:{tag} .")


@task
def run(ctx: Context, mode: str = "production", port: int = 8080, tag: str = IMAGE_TAG) -> None:
    """Run the container image."""
    ctx.run(f"docker run --rm --env-file .env.{mode} -p {port}:8080 {ctx.project.repository}:{tag}")


@task(pre=[build, run], default=True)
def all(_: Context) -> None:
    """Run all container tasks."""
