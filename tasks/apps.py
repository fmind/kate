"""App tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def expose(ctx: Context) -> None:
    """Expose the application on the internet."""
    ctx.run(f"ngrok start --config=ngrok.yml {ctx.project.repository}")


@task(pre=[expose], default=True)
def all(_: Context) -> None:
    """Run all app tasks."""
