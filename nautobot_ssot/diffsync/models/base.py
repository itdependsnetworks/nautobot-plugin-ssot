"""Models commonly used in SSoT plugins."""
from lib2to3.pgen2.token import OP
from diffsync import DiffSyncModel
from typing import List, Optional


class Site(DiffSyncModel):
    """Site Model based on DiffSyncModel.

    A site must have a unique name and can be composed of Vlans.
    """

    _modelname = "site"
    _identifiers = ("slug",)
    _attributes = ("name", "status")
    _children = {"vlan": "vlans", "device": "devices"}

    slug: str
    name: str
    vlans: List[str] = []
    devices: List = []
    status: str


class Device(DiffSyncModel):
    """Device Model based on DiffSyncModel.

    A device must have a unique name and can be part of a site.
    """

    _modelname = "device"
    _identifiers = ("name",)
    _attributes = ("site",)
    _children = {"interface": "interfaces"}

    name: str
    site: Optional[str]
    interfaces: List = []


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

    description: Optional[str]
    mode: Optional[str]
    tagged_vlans: List[str] = []
    untagged_vlan: Optional[str]
    type: str

    status: str


class Vlan(DiffSyncModel):
    """Vlan Model based on DiffSyncModel.

    An Vlan must be associated with a Site and the vlan_id msut be unique within a site.
    """

    _attributes = ("name", "status")
    _modelname = "vlan"
    _identifiers = ("site", "vid")

    site: str
    vid: int
    name: Optional[str]
    status: str


class Status(DiffSyncModel):
    """Status Model based on DiffSyncModel.

    A status must have a unique name and can be composed of Vlans and Prefixes.
    """

    _modelname = "status"
    _identifiers = ("slug",)
    _attributes = ("name",)

    slug: str
    name: str
