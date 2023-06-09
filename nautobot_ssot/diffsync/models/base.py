"""Models commonly used in SSoT plugins."""

from nautobot_ssot.diffsync.models.apps.dcim_location import Site, Region, Location, LocationType
from nautobot_ssot.diffsync.models.apps.dcim_device import (
    Device,
    Interface,
    DeviceType,
    Manufacturer,
    Platform,
    DeviceRole,
    DeviceRedundancyGroup,
)
from nautobot_ssot.diffsync.models.apps.extras import Status, Tag
from nautobot_ssot.diffsync.models.apps.ipam import Vlan

__all__ = (
    "Device",
    "DeviceRedundancyGroup",
    "DeviceRole",
    "DeviceType",
    "Interface",
    "Location",
    "LocationType",
    "Manufacturer",
    "Platform",
    "Region",
    "Site",
    "Status",
    "Tag",
    "Vlan",
)
