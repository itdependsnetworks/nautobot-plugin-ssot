"""Model mixins for Nautobot models with SSoT."""
from django.db.models.base import Model
from typing import Optional


class DiffSyncModelMixIn:
    """MixIn class to handle sync generically."""

    _orm_model = None
    _foreign_key = {}
    _many_to_many = {}
    _generic_relation = {}
    _unique_fields = ("pk",)
    _skip = []

    pk: Optional[str]

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Method to handle generically."""
        model = super().create(ids=ids, diffsync=diffsync, attrs=attrs)
        # model is the DiffSyncModel instance, which has data about the instance required
        db_model = cls._orm_model
        if not db_model:
            raise ValueError(f"The attribute `_orm_model` was not set on {cls.__name__}")
        obj = db_model()
        instance_values = {**ids, **attrs}
        combined = cls.combined_keys(model)
        for key, value in instance_values.items():
            if hasattr(model, "_skip") and key in model._skip:
                continue
            if key not in combined:
                setattr(obj, key, value)
            else:
                if not value:  # need to find the value of the other object, if none exists, that won't work
                    continue
                if key in list(model._generic_relation.keys()):
                    with_parent = {
                        key: model._generic_relation[key]["parent"] for key in list(model._generic_relation.keys())
                    }
                    with_values = "__".join(
                        [instance_values[key] for key in list(model._generic_relation[key]["identifiers"])]
                    )
                    db_obj = cls.get_fk(with_parent, diffsync, key, with_values)
                    setattr(obj, model._generic_relation[key]["attr"], db_obj)
                if key in list(model._foreign_key.keys()):
                    db_obj = cls.get_fk(model._foreign_key, diffsync, key, value)
                    setattr(obj, key, db_obj)
                if key in list(model._many_to_many.keys()):
                    if isinstance(value, list):
                        for val in value:
                            db_obj = cls.get_fk(model._many_to_many, diffsync, key, val)
                            getattr(obj, key).add(db_obj)
                    else:
                        db_obj = cls.get_fk(model._many_to_many, diffsync, key, value)
                        obj.set(db_obj)
        try:
            obj.validated_save()
        except:
            print(cls._orm_model)
            print(obj)
        if not model.pk:
            setattr(model, "pk", obj.pk)
        return model

    def update(self, attrs):  # pylint: disable=too-many-branches
        """Create Method to handle generically."""
        db_model = self._orm_model
        if not db_model:
            raise ValueError(f"The attribute `_orm_model` was not set on {self.__name__}")
        # Simply doing this to make the code in the update and add more similar
        diffsync = self.diffsync
        instance_values = attrs.copy()
        combined = self.combined_keys(self)
        var_by_pk = self.get_identifiers()

        for key, val in var_by_pk.items():
            if key in list(self._foreign_key.keys()):
                db_obj = self.get_fk(self._foreign_key, diffsync, key, val)
                var_by_pk[key] = str(db_obj.pk)
            if key in list(self._many_to_many.keys()):
                db_obj = self.get_fk(self._many_to_many, diffsync, key, val)
                var_by_pk[key] = str(db_obj.pk)

        obj = db_model.objects.get(**var_by_pk)

        for key, value in instance_values.items():
            if hasattr(self, "_skip") and key in self._skip:
                continue
            if key not in combined:
                setattr(obj, key, value)
            else:
                if not value:  # need to find the value of the other object, if none exists, that won't work
                    continue
                if key in list(self._generic_relation.keys()):
                    with_parent = {
                        key: self._generic_relation[key]["parent"] for key in list(self._generic_relation.keys())
                    }
                    with_values = "__".join(
                        [instance_values[key] for key in list(self._generic_relation[key]["identifiers"])]
                    )
                    db_obj = self.get_fk(with_parent, diffsync, key, with_values)
                    setattr(obj, self._generic_relation[key]["attr"], db_obj)
                if key in list(self._foreign_key.keys()):
                    db_obj = self.get_fk(self._foreign_key, diffsync, key, value)
                    setattr(obj, key, db_obj)
                if key in list(self._many_to_many.keys()):
                    if isinstance(value, list):
                        for val in value:
                            db_obj = self.get_fk(self._many_to_many, diffsync, key, val)
                            getattr(obj, key).add(db_obj)
                    else:
                        db_obj = self.get_fk(self._many_to_many, diffsync, key, value)
                        obj.set(db_obj)
        obj.save()
        return super().update(attrs)

    def delete(self):
        """Create Method to handle generically."""
        db_model = self._orm_model
        if not db_model:
            raise ValueError(f"The attribute `_orm_model` was not set on {self.__name__}")
        obj = db_model.objects.get(pk=self.pk)
        obj.delete()

        super().delete()
        return self

    @staticmethod
    def get_fk(fks, diffsync, key, value):
        """Function to get the fk of an object, given information stored in ORM."""
        # fks comes from self._foreign_keys
        # key matches a key in `_foreign_keys` which is the local attribute
        # value is the get_unique_id() we are looking for
        if key in list(fks.keys()):
            model_name = [val for _key, val in fks.items() if _key == key][0]
            # key_model = diffsync.meta[model]

            model = diffsync.get(model_name, value)
            key_model = model._orm_model
            pkey = model.pk
            return key_model.objects.get(pk=pkey)

    @staticmethod
    def combined_keys(obj):
        """These are a series of sanity checks to ensure check for things what would cause an issue."""
        # TODO: Make more descriptive errors that include the value to make easier to find
        fk_set = set(list(obj._foreign_key.keys()))
        mtm_set = set(list(obj._many_to_many.keys()))
        gfk_set = set(list(obj._generic_relation.keys()))
        if bool(fk_set.intersection(mtm_set)):
            raise ValueError("There are matching keys in mutual exclusive dictionaries")
        if bool(fk_set.intersection(gfk_set)):
            raise ValueError("There are matching keys in mutual exclusive dictionaries")
        if bool(mtm_set.intersection(gfk_set)):
            raise ValueError("There are matching keys in mutual exclusive dictionaries")
        if not hasattr(obj, "_orm_model"):
            raise ValueError("The `_orm_model` attribute was not set.")
        if not issubclass(obj._orm_model, Model):
            raise ValueError(
                f"The `_orm_model` attribute value: `{obj._orm_model}` is not a Django an instance of `django.db.models.base.Model` {obj._orm_model.mro()}"
            )
        _combined_keys = set(list(fk_set) + list(mtm_set) + list(gfk_set))
        return _combined_keys
