"""DiffSync adapter mixins."""
from diffsync.enum import DiffSyncFlags, DiffSyncModelFlags


class DiffSyncMixIn:
    """Mixin to update add to allow for 'stuffing' data based on unique fields."""

    _unique_data = {}

    def add(self, obj, *args, **kwargs):
        """Override add method to stuff data into dictionary based on the `_unique_fields`."""
        super().add(obj, *args, **kwargs)
        modelname = obj._modelname

        for attr in getattr(obj, "_unique_fields", []):
            if hasattr(obj, attr):
                if not self._unique_data.get(modelname):
                    self._unique_data[modelname] = {}
                if not self._unique_data[modelname].get(attr):
                    self._unique_data[modelname][attr] = {}
                self._unique_data[modelname][attr][getattr(obj, attr)] = obj


class AdapterMixIn:
    """Simple pass2 docstring."""

    def apply_diffsync_flags(self):
        """Helper function for DiffSync Flag assignment."""
        if not self.diffsync_flags:
            return
        for item in self.diffsync_flags:
            if not hasattr(DiffSyncFlags, item):
                raise ValueError(f"There was an attempt to add a non-existing flag of `{item}`")
            self.global_flags |= getattr(DiffSyncFlags, item)

    def apply_model_flags(self, obj, tags):
        """Helper function for DiffSync Flag assignment on model instances."""
        if not self.diffsync_model_flags:
            return
        for item in tags:
            if not hasattr(DiffSyncModelFlags, item):
                continue
            obj.model_flags |= getattr(DiffSyncModelFlags, item)
        if not self.diffsync_model_flags.get(obj._modelname):
            return
        for item in self.diffsync_model_flags[obj._modelname]:
            if not hasattr(DiffSyncModelFlags, item):
                raise ValueError(f"There was an attempt to add a non-existing flag of `{item}`")
            obj.model_flags |= getattr(DiffSyncModelFlags, item)
