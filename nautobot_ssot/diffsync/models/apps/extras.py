"""Nautobot Extras base models."""
from diffsync import DiffSyncModel
from typing import Optional


class Status(DiffSyncModel):
    """Status Model based on DiffSyncModel.

    A status must have a unique name and can be composed of Vlans and Prefixes.
    """

    _modelname = "status"
    _identifiers = ("slug",)
    _attributes = ("name",)

    slug: str
    name: str


class Tag(DiffSyncModel):
    """Status Model based on DiffSyncModel.

    A status must have a unique name.
    """

    _modelname = "status"
    _identifiers = ("slug",)
    _attributes = ("name", "description", "color")

    slug: str
    name: str
    description: Optional[str] = ""
    color: Optional[str]
