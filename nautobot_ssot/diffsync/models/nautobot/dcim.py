"""Nautobot ORM models commonly used in SSoT plugins."""

from nautobot.dcim import models as dcim_models
from nautobot_ssot.diffsync.models.mixins import DiffSyncModelMixIn
from typing import Optional

from nautobot_ssot.diffsync.models.base import (
    Site,
    Region,
    LocationType,
    Location,
    Device,
    DeviceRedundancyGroup,
    DeviceRole,
    DeviceType,
    Interface,
    Manufacturer,
    Platform,
)


###########################
# apps/dcim_location
###########################


class NautobotLocation(DiffSyncModelMixIn, Location):
    """Simple pass2 docstring."""

    _orm_model = dcim_models.Location
    _foreign_key = {"tenant": "tenant", "site": "site", "location": "location_type"}
    pk: Optional[str]


class NautobotLocationType(DiffSyncModelMixIn, LocationType):
    """Simple pass2 docstring."""

    _orm_model = dcim_models.LocationType
    _many_to_many = {"content_types": "contenttype"}
    pk: Optional[str]


class NautobotSite(DiffSyncModelMixIn, Site):
    """Simple pass2 docstring."""

    _foreign_key = {"status": "status", "tenant": "tenant", "region": "region"}
    _orm_model = dcim_models.Site
    pk: Optional[str]


class NautobotRegion(DiffSyncModelMixIn, Region):
    """Simple pass2 docstring."""

    _foreign_key = {"region": "parent"}
    _orm_model = dcim_models.Region
    pk: Optional[str]


###########################
# apps/dcim_device
###########################


class NautobotDevice(DiffSyncModelMixIn, Device):
    """Simple pass3 docstring."""

    _foreign_key = {
        "device_type": "device_type",
        "device_role": "device_role",
        "site": "site",
        "status": "status",
        "platform": "platform",
        "tenant": "tenant",
    }
    _orm_model = dcim_models.Device
    pk: Optional[str]


class NautobotDeviceRedundancyGroup(DiffSyncModelMixIn, DeviceRedundancyGroup):
    """Simple pass3 docstring."""

    _orm_model = dcim_models.DeviceRedundancyGroup
    pk: Optional[str]


class NautobotDeviceRole(DiffSyncModelMixIn, DeviceRole):
    """Extenstion of the DeviceRole model."""

    _orm_model = dcim_models.DeviceRole
    pk: Optional[str]


class NautobotDeviceType(DiffSyncModelMixIn, DeviceType):
    """Extension of the Status model."""

    _orm_model = dcim_models.DeviceType
    _foreign_key = {"manufacturer": "manufacturer"}
    pk: Optional[str]


class NautobotInterface(DiffSyncModelMixIn, Interface):
    """Simple pass4 docstring."""

    _orm_model = dcim_models.Interface
    _foreign_key = {"device": "device", "untagged_vlan": "vlan", "status": "status"}
    _many_to_many = {"tagged_vlans": "vlan"}
    pk: Optional[str]


class NautobotManufacturer(DiffSyncModelMixIn, Manufacturer):
    """Extension of the Manufacturer model."""

    _orm_model = dcim_models.Manufacturer
    pk: Optional[str]


class NautobotPlatform(DiffSyncModelMixIn, Platform):
    """Extension of the Platform model."""

    _orm_model = dcim_models.Platform
    pk: Optional[str]
    _foreign_key = {"manufacturer": "manufacturer"}
