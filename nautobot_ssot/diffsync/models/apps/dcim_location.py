"""Models commonly used in SSoT plugins."""
from diffsync import DiffSyncModel
from typing import List, Optional


class Location(DiffSyncModel):
    """Location Model based on DiffSyncModel.

    A location must have a unique name.
    """

    _modelname = "location"
    _identifiers = ("slug",)
    _attributes = ("name", "location_type", "description", "site", "tenant")
    _children = {"location": "locations"}

    description: Optional[str]
    slug: str
    name: str
    location_type: str
    site: Optional[str]
    tenant: Optional[str]
    locations: List[str] = []


class LocationType(DiffSyncModel):
    """LocationType Model based on DiffSyncModel.

    A locationtype must have a unique name.
    """

    _modelname = "locationtype"
    _identifiers = ("slug",)
    _attributes = ("name", "content_types", "description", "nestable")
    _children = {"location": "locations"}

    description: Optional[str]
    slug: str
    name: str
    nestable: bool
    content_types: List[str] = []
    locations: List[str] = []


class Region(DiffSyncModel):
    """Region Model based on DiffSyncModel.

    A region must have a unique name.
    """

    _modelname = "region"
    _identifiers = ("slug",)
    _attributes = (
        "name",
        "parent",
        "description",
    )
    _children = {"region": "children", "site": "sites"}
    description: Optional[str]
    parent: Optional[str]
    slug: str
    name: str
    children: List[str] = []
    sites: List[str] = []


class Site(DiffSyncModel):
    """Site Model based on DiffSyncModel.

    A site must have a unique name and can be composed of Vlans.
    """

    _modelname = "site"
    _identifiers = ("slug",)
    _attributes = (
        "name",
        "status",
        "region",
        "tenant",
        "facility",
        "asn",
        "description",
        "time_zone",
        "physical_address",
        "shipping_address",
        "latitude",
        "longitude",
        "contact_name",
        "contact_phone",
        "contact_email",
        "comments",
    )
    _children = {"vlan": "vlans", "device": "devices"}

    slug: str
    name: str
    vlans: List[str] = []
    devices: List = []
    status: str
    region: Optional[str]
    tenant: Optional[str]
    facility: Optional[str]
    asn: Optional[str]
    description: Optional[str]
    physical_address: Optional[str]
    shipping_address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    comments: Optional[str]
