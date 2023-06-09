"""Nautobot ORM models commonly used in SSoT plugins."""
from nautobot.extras import models as extras_models
from nautobot_ssot.diffsync.models.mixins import DiffSyncModelMixIn
from typing import Optional

from nautobot_ssot.diffsync.models.base import (
    Status,
    Tag,
)


class NautobotStatus(DiffSyncModelMixIn, Status):
    """Extension of the Status model."""

    _orm_model = extras_models.Status
    _unique_fields = ("pk", "name")
    pk: Optional[str]


class NautobotTag(DiffSyncModelMixIn, Tag):
    """Extension of the Tag model."""

    _orm_model = extras_models.Tag
    _unique_fields = ("pk", "name")
    pk: Optional[str]
