"""Models commonly used in SSoT plugins."""
from diffsync import DiffSyncModel
from typing import List, Optional


class Device(DiffSyncModel):
    """Device Model based on DiffSyncModel.

    A device must have a unique name and can be part of a site.
    """

    _modelname = "device"
    _identifiers = ("name",)
    _attributes = (
        "site",
        "device_type",
        "device_role",
        "status",
        "device_redundancy_group",
        "device_redundancy_group_priority",
    )
    _children = {"interface": "interfaces"}

    name: str
    status: str
    site: Optional[str]
    device_type: Optional[str]
    device_role: Optional[str]
    interfaces: List = []
    device_redundancy_group_priority: Optional[str]
    device_redundancy_group: Optional[str]


class DeviceRedundancyGroup(DiffSyncModel):
    """DeviceRedundancyGroup Model based on DiffSyncModel.

    A deviceredundancygroup must have a unique name and can be part of a site.
    """

    _modelname = "deviceredundancygroup"
    _identifiers = ("name",)
    _attributes = ("slug", "description", "failover_strategy", "comments")

    name: str
    description: Optional[str] = ""
    failover_strategy: Optional[str] = ""
    comments: Optional[str] = ""


class DeviceRole(DiffSyncModel):
    """Manufacturer Model based on DiffSyncModel.

    A DeviceRole must have a unique name.
    """

    _modelname = "device_role"
    _identifiers = ("slug",)
    _attributes = ("name",)
    _children = {"device": "devices"}

    slug: str
    name: str
    devices: List = []


class DeviceType(DiffSyncModel):
    """DeviceType Model based on DiffSyncModel.

    A device_type must have a unique name.
    """

    _modelname = "device_type"
    _identifiers = ("slug",)
    _attributes = ("model", "manufacturer")
    _children = {"device": "devices"}

    slug: str
    model: str
    manufacturer: str
    devices: List = []


class Interface(DiffSyncModel):  # pylint: disable=too-many-instance-attributes
    """Interface Model based on DiffSyncModel.

    An interface must be attached to a device and the name must be unique per device.
    """

    _modelname = "interface"
    _identifiers = ("device", "name")
    _shortname = ("name",)
    _attributes = (
        "description",
        "mode",
        "tagged_vlans",
        "untagged_vlan",
        "type",
        "status",
    )
    _children = {}

    device: str
    name: str

    description: Optional[str] = ""
    mode: str
    tagged_vlans: List[str] = []
    untagged_vlan: Optional[str] = ""
    type: str

    status: str


class Manufacturer(DiffSyncModel):
    """Manufacturer Model based on DiffSyncModel.

    A manufacturer must have a unique name.
    """

    _modelname = "manufacturer"
    _identifiers = ("slug",)
    _attributes = ("name",)
    _children = {"device_type": "device_types"}

    slug: str
    name: str
    device_types: List = []
