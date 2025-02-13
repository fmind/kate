"""Task collections of the project."""

# mypy: ignore-errors

# %% IMPORTS

from invoke import Collection

from . import (
    apps,
    checks,
    cleans,
    clients,
    containers,
    docs,
    formats,
    installs,
    packages,
    servers,
    spiders,
)

# %% NAMESPACES

ns = Collection()

# %% COLLECTIONS

ns.add_collection(apps)
ns.add_collection(checks)
ns.add_collection(cleans)
ns.add_collection(clients)
ns.add_collection(containers)
ns.add_collection(docs)
ns.add_collection(formats)
ns.add_collection(installs)
ns.add_collection(packages)
ns.add_collection(servers, default=True)
ns.add_collection(spiders)
