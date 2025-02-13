"""Client tasks of the project."""

# %% IMPORTS

from invoke.context import Context
from invoke.tasks import task

# %% TASKS


@task
def install(ctx: Context) -> None:
    """Install the project client."""
    with ctx.cd("client"):
        ctx.run("yarn install")


@task
def dev(ctx: Context) -> None:
    """Start the project client."""
    with ctx.cd("client"):
        ctx.run("yarn run dev")


@task
def build(ctx: Context) -> None:
    """Build the project client."""
    with ctx.cd("client"):
        out_dir = f"../src/{ctx.project.package}/clients"
        ctx.run(f"yarn run build --outDir={out_dir} --emptyOutDir")


@task
def lint(ctx: Context) -> None:
    """Lint the project client."""
    with ctx.cd("client"):
        ctx.run("yarn run lint")


@task(pre=[build])
def preview(ctx: Context) -> None:
    """Preview the project client."""
    with ctx.cd("client"):
        ctx.run("yarn run preview")


@task(pre=[dev], default=True)
def all(_: Context) -> None:
    """Run all client tasks."""
