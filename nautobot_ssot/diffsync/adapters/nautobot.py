"""Nautobot DiffSync adapters."""
from diffsync import DiffSync
from nautobot.core.graphql import execute_query
from nautobot.extras import models as extras_models
import re

from nautobot_ssot.diffsync.models.nautobot import (
    NautobotDevice,
    NautobotInterface,
    NautobotSite,
    NautobotStatus,
    NautobotVlan,
)

SITE_QUERY = """{
  sites {
    name
    slug
    id
    status {
      slug
    }
    devices {
      name
      id
      interfaces {
        name
        id
        mode
        description
        type
        tagged_vlans {
          id
          name
          vid
        }
        untagged_vlan {
          id
          name
          vid
        }
        status {
          slug
          id
        }
        tags {
          name
        }
      }
      status {
        slug
        id
      }
      tags {
        name
        id
      }
    }
    vlans {
      id
      vid
      name
      status {
        slug
        id
      }
      tags {
        name
      }
    }
    tags {
      name
      id
    }
  }
}"""


class NautobotAdapter(DiffSync):
    """DiffSync adapter class for loading data from the local Nautobot instance."""

    # Model classes used by this adapter class
    site = NautobotSite
    device = NautobotDevice
    interface = NautobotInterface
    vlan = NautobotVlan
    status = NautobotStatus

    # Top-level class labels, i.e. those classes that are handled directly rather than as children of other models
    top_level = ("status", "site")

    def __init__(self, *args, job=None, request, **kwargs):
        """Instantiate this class, but do not load data immediately from the local system."""
        super().__init__(*args, **kwargs)
        self.job = job
        self.request = request

    def load(self):
        """Load Region and Site data from the local Nautobot instance."""
        for status in extras_models.Status.objects.all():
            _st = self.status(slug=status.slug, name=status.name, pk=str(status.pk))
            self.add(_st)

        for site_gql in execute_query(query=SITE_QUERY, request=self.request).data["sites"]:
            site = self.site(
                slug=site_gql["slug"], name=site_gql["name"], pk=site_gql["id"], status=site_gql["status"]["slug"]
            )
            self.add(site)
            for vlan_gql in site_gql["vlans"]:
                vlan = self.vlan(
                    vid=vlan_gql["vid"],
                    name=vlan_gql["name"],
                    status=vlan_gql["status"]["slug"],
                    pk=vlan_gql["id"],
                    site=site_gql["slug"],
                )
                self.add(vlan)
                site.add_child(vlan)
            for device_gql in site_gql["devices"]:
                device = self.device(
                    name=device_gql["name"],
                    pk=device_gql["id"],
                    site=site_gql["slug"],
                    status=device_gql["status"]["slug"],
                )
                self.add(device)
                site.add_child(device)
                for interface_gql in device_gql["interfaces"]:
                    interface = self.interface(
                        name=interface_gql["name"],
                        description=interface_gql["description"],
                        mode=interface_gql["mode"].lower(),
                        tagged_vlans=[vlan["vid"] for vlan in interface_gql.get("tagged_vlans", [])],
                        untagged_vlan=interface_gql["untagged_vlan"]["vid"]
                        if interface_gql.get("untagged_vlan")
                        else None,
                        status=interface_gql["status"]["slug"],
                        pk=interface_gql["id"],
                        device=device_gql["name"],
                        type=re.sub(r"^A_", "", interface_gql["type"]).lower().replace("_", "-"),
                    )
                    self.add(interface)
                    device.add_child(interface)

        # self.job.log_debug(message=f"Loaded {site_model} from local Nautobot instance")
