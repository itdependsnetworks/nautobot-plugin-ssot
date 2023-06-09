"""Models commonly used in SSoT plugins."""
from diffsync import DiffSyncModel
from typing import Optional


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
