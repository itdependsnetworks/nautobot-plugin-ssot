"""Nautobot ORM models commonly used in SSoT plugins."""

from nautobot.ipam import models as ipam_models
from nautobot_ssot.diffsync.models.mixins import DiffSyncModelMixIn
from typing import Optional

from nautobot_ssot.diffsync.models.base import Vlan


class NautobotVlan(DiffSyncModelMixIn, Vlan):
    """Simple pass5 docstring."""

    _orm_model = ipam_models.VLAN
    _foreign_key = {"site": "site", "status": "status"}
    pk: Optional[str]
