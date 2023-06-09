"""Sample data-source and data-target Jobs based on models & adaptes provided by plugin."""
# Skip colon check for multiple statements on one line.
# flake8: noqa: E701

from django.templatetags.static import static

from diffsync import DiffSync
from nautobot.extras.jobs import Job

from nautobot_ssot.jobs.base import DataSource
from nautobot_ssot.diffsync.adapters.nautobot import NautobotAdapter
from nautobot_ssot.diffsync.models.base import Site, Device, Interface, Vlan

from nautobot_ssot.tests.mock.basic import data as example_data

name = "SSoT MixIn Examples"  # pylint: disable=invalid-name


class DictionaryLocal(DiffSync):
    """DiffSync adapter class for loading data from the local Nautobot instance."""

    # Model classes used by this adapter class
    site = Site
    device = Device
    interface = Interface
    vlan = Vlan

    top_level = ("site",)

    def __init__(self, *args, job=None, data, **kwargs):
        """Instantiate this class, but do not load data immediately from the local system."""
        super().__init__(*args, **kwargs)
        self.job = job
        self.data = data

    def load(self):
        """Simple pass7 docstring."""
        self.load_from_dict(self.data)


class SyncFromDictionary(DataSource, Job):
    """Sync Region and Site data from a remote Nautobot instance into the local Nautobot instance."""

    class Meta:
        """Metaclass attributes of ExampleDataSource."""

        name = "Sync from Dictionary to local instance"
        description = 'Example "data source" Job for loading data into Nautobot from a Python dictionary.'
        data_source = "Python Dictionary"
        data_source_icon = static("nautobot_ssot/dictionary_logo.png")
        data_target = "Nautobot (orm)"
        data_target_icon = static("img/nautobot_logo.png")

    # @classmethod
    # def data_mappings(cls):
    #     """This Job maps Region and Site objects from the remote system to the local system."""
    #     return (
    #         DataMapping("Region (remote)", None, "Region (local)", reverse("dcim:region_list")),
    #         DataMapping("Site (remote)", None, "Site (local)", reverse("dcim:site_list")),
    #         DataMapping("Prefix (remote)", None, "Prefix (local)", reverse("ipam:prefix_list")),
    #     )

    def load_source_adapter(self):
        """Method to instantiate and load the SOURCE adapter into `self.source_adapter`."""
        self.source_adapter = DictionaryLocal(job=self, data=example_data)
        self.source_adapter.load()

    def load_target_adapter(self):
        """Method to instantiate and load the TARGET adapter into `self.target_adapter`."""
        self.target_adapter = NautobotAdapter(job=self, request=self.request)
        self.target_adapter.load()

    # def lookup_object(self, model_name, unique_id):
    #     """Look up a Nautobot object based on the DiffSync model name and unique ID."""
    #     if model_name == "region":
    #         try:
    #             return Region.objects.get(name=unique_id)
    #         except Region.DoesNotExist:
    #             pass
    #     elif model_name == "site":
    #         try:
    #             return Site.objects.get(name=unique_id)
    #         except Site.DoesNotExist:
    #             pass
    #     elif model_name == "prefix":
    #         try:
    #             return Prefix.objects.get(
    #                 prefix=unique_id.split("__")[0], tenant__slug=unique_id.split("__")[1] or None
    #             )
    #         except Prefix.DoesNotExist:
    #             pass
    #     return None
