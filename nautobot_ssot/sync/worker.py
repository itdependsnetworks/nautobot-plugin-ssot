"""Base/generic functionality for implementation of a data synchronization worker class."""
from collections import OrderedDict

from django.utils.functional import classproperty

from nautobot.extras.choices import LogLevelChoices
from nautobot.extras.jobs import ScriptVariable

from nautobot_ssot.forms import SyncForm
from nautobot_ssot.models import SyncLogEntry


class DataSyncWorker:
    """Semi-abstract base class to serve as a parent for all data sync worker implementations."""

    # Django: when passed this class or one of its subclasses as context for a template,
    # DO NOT automatically instantiate it!
    do_not_call_in_templates = True

    def __init__(self, sync=None, data=None):
        """Instantiate a DataSyncWorker in preparation for executing the data sync.

        Args:
            sync (Sync): Database object that will be used to track the progress of the data sync.
            data (dict): Key-value pairs of parameters passed into this worker
        """
        self.sync = sync
        self.data = data
        self.dry_run = data.get("dry_run", True) if data else True

    class Meta:
        """Metaclass attributes of a DataSyncWorker.

        Fields that can be defined here, and their default values if undefined, include:
        - dry_run_default (True) - Default value for "dry_run" when rendering as a form.
        - name (cls.__name__) - Short name of this worker class.
        - slug (cls.__name__) - URL-safe unique identifier of this worker class.
        - description ("")- Detailed description of this worker class.
        """

        dry_run_default = True

    @classproperty
    def name(cls):
        """Short name of this worker."""
        return getattr(cls.Meta, "name", cls.__name__)

    @classproperty
    def slug(cls):
        """URL-safe unique identifier of this worker."""
        return getattr(cls.Meta, "slug", cls.__name__.lower())

    @classproperty
    def description(cls):
        """Detailed description of this worker."""
        return getattr(cls.Meta, "description", "")

    @classmethod
    def _get_vars(cls):
        """Get the dictionary of ScriptVariable attributes on this class."""
        vars = OrderedDict()
        for name, attr in cls.__dict__.items():
            if isinstance(attr, ScriptVariable):
                vars[name] = attr
        return vars

    @classmethod
    def as_form(cls, *args, **kwargs):
        """Construct a Django form suitable for providing any input parameters required.

        args and kwargs are passed through to the Form constructor.

        Heavily based on nautobot.extras.jobs.Job.as_form().
        """
        fields = {name: var.as_field() for name, var in cls._get_vars().items()}
        # Create a new Form class inheriting from SyncForm with fields as its attributes
        FormClass = type("SyncForm", (SyncForm,), fields)
        # Instantiate the Form class
        form = FormClass(*args, **kwargs)

        # Set initial value of "dry run" checkbox
        form.fields["dry_run"].initial = getattr(cls.Meta, "dry_run_default", True)

        return form

    @property
    def job_result(self):
        return self.sync.job_result

    def job_log(
        self,
        message,
        object=None,
        level=LogLevelChoices.LOG_DEFAULT,
        grouping="sync",
        logger=None,
    ):
        """Log a status message to the JobResult record."""
        self.job_result.log(message, obj=object, level_choice=level, grouping=grouping, logger=logger)

    def sync_log(
        self,
        action,
        status,
        message="",
        diff=None,
        synced_object=None,
        object_repr=None,
        object_change=None,
    ):
        """Log a action message as a SyncLogEntry."""
        if not diff:
            diff = {}
        if synced_object and not object_repr:
            object_repr = repr(synced_object)

        SyncLogEntry.objects.create(
            sync=self.sync,
            action=action,
            status=status,
            message=message,
            diff=diff,
            synced_object=synced_object,
            object_repr=object_repr,
            object_change=object_change,
        )

    #
    # Methods to be implemented by subclasses, below:
    #

    def execute(self):
        """Perform a dry run or actual data synchronization, depending on self.dry_run.

        Note that unlike a Nautobot Job, it is up to the implementation to provide dry-run behavior;
        since execution may involve manipulation of data in other systems, Nautobot cannot itself
        guarantee proper rollback or other dry-run behavior on its own.
        """

    def lookup_object(self, model_name, unique_id):
        """Look up the Nautobot record and associated ObjectChange, if any, identified by the args.

        Optional helper method used to build more detailed/accurate SyncLogEntry records from DiffSync logs.

        Args:
            model_name (str): DiffSyncModel class name or similar class/model label.
            unique_id (str): DiffSyncModel unique_id or similar unique identifier.

        Returns:
            tuple: (nautobot_record, nautobot_objectchange_record). Either or both may be None.
        """
        return (None, None)