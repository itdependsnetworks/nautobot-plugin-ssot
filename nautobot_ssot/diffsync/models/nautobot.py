"""Nautobot ORM models commonly used in SSoT plugins."""

from nautobot.dcim import models as dcim_models
from nautobot.ipam import models as ipam_models
from nautobot.extras import models as extras_models
from nautobot_ssot.diffsync.models.mixins import DiffSyncModelMixIn
from typing import Optional

from nautobot_ssot.diffsync.models.base import (
    Site,
    Device,
    Interface,
    Vlan,
    Status,
    DeviceRole,
    DeviceType,
    Manufacturer,
)


class NautobotSite(DiffSyncModelMixIn, Site):
    """Simple pass2 docstring."""

    _foreign_key = {"status": "status"}
    _orm_model = dcim_models.Site
    pk: Optional[str]


class NautobotDevice(DiffSyncModelMixIn, Device):
    """Simple pass3 docstring."""

    _foreign_key = {"status": "status"}
    _orm_model = dcim_models.Device
    pk: Optional[str]


class NautobotInterface(DiffSyncModelMixIn, Interface):
    """Simple pass4 docstring."""

    _orm_model = dcim_models.Interface
    _foreign_key = {"device": "device", "untagged_vlan": "vlan", "status": "status"}
    _many_to_many = {"tagged_vlans": "vlan"}
    pk: Optional[str]


class NautobotVlan(DiffSyncModelMixIn, Vlan):
    """Simple pass5 docstring."""

    _orm_model = ipam_models.VLAN
    _foreign_key = {"site": "site", "status": "status"}
    pk: Optional[str]


class NautobotStatus(Status):
    """Extension of the Status model."""

    _orm_model = extras_models.Status
    _unique_fields = ("pk",)
    _attributes = ("pk", "name")
    pk: Optional[str]


class NautobotDeviceType(DiffSyncModelMixIn, DeviceType):
    """Extension of the Status model."""

    _orm_model = dcim_models.DeviceType
    _foreign_key = {"manufacturer": "manufacturer"}
    pk: Optional[str]


class NautobotManufacturer(DiffSyncModelMixIn, Manufacturer):
    """Extension of the Manufacturer model."""

    _orm_model = dcim_models.Manufacturer
    pk: Optional[str]


class NautobotDeviceRole(DiffSyncModelMixIn, DeviceRole):
    """Extenstion of the DeviceRole model."""

    _orm_model = dcim_models.DeviceRole
    pk: Optional[str]
