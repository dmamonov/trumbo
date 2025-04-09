from abc import abstractmethod, ABC
from typing import TypeVar

from django.core.paginator import Paginator
from django.db.models import QuerySet, Model
from django.utils.timezone import now

Serializer = TypeVar("Serializer")


class IService(ABC):
    @property
    @abstractmethod
    def model(self) -> Model:
        ...


class Service(IService, ABC):
    """
    Base Class for all services.

    Implements the most common functions
    :model Django Model
    """

    _results: tuple = []
    _context: dict = {}
    _total: int = 0
    _serializer: Serializer = None

    def serializer(self, serializer: Serializer, **context):
        """
        Set the serializer to format the data
        if you don't set it, it returns the ORM's objects
        :param serializer: Serializer: Serializer object
        :return: Service
        """
        self._serializer = serializer
        self._context = context
        return self

    def find_all(self, return_object: bool = False, **kwargs):
        """

        :param return_object: Return Django ORM objects
        :param kwargs: Filters and Excludes params for queryset
        :return: Self object instance.
        """
        # Filters and excludes params
        filters = kwargs.get("filters", {})
        excludes = kwargs.get("excludes", {})

        # Get all elements from BD
        all_elements = self.model.objects.filter(deleted=False, **filters).exclude(**excludes)

        # Order all elements
        all_elements = all_elements.order_by("pk")
        if (kwargs.get("sort") and kwargs.get("order") and not isinstance(kwargs.get("sort"), list)):
            # Ordena los elementos
            sort = kwargs.pop("sort")
            order = kwargs.pop("order")
            if order == "desc":
                sort = "-" + sort
            all_elements = all_elements.order_by(sort)

        if kwargs.get("sort") and isinstance(kwargs["sort"], list):
            # Ordena los elementos
            sort = kwargs.pop("sort")
            all_elements = all_elements.order_by(*sort)

        # Return Django ORM object
        if return_object or not self._serializer:
            return all_elements

        self._results = all_elements

    def paginate(self, limit: int = 100, offset: int = 0, data=None):
        """
        Paginate elements.
        if data argument is provided, execute the paginate over the data
        :param limit: Limit to paginate
        :param offset: Offset to paginate
        :param data: List of elements to paginate
        :return:
        """
        if data is None:
            data = []
        page = 0
        if offset == 0:
            page = 1
        elif offset == limit:
            page = 2
        elif offset > limit:
            page = (offset + limit) / limit
        if data:
            paginator = Paginator(data, limit)
        else:
            paginator = Paginator(self._results, limit)
        elements = paginator.get_page(page)

        if not self._serializer:
            return elements.object_list, paginator.count

        self._results = elements.object_list
        self._total = paginator.count
        if self._serializer:
            return self.json()
        return self._results, self._total

    def find_by(self, return_object: bool = False, **kwargs):
        """
        Get one element from the DB
        :param return_object: Return Django ORM objects
        :param kwargs: Filters params to query
        :return:
        """
        try:
            self.before_get()
            self._results = self.model.objects.get(deleted=False, **kwargs)
            if return_object or not self._serializer:
                return self._results
            items = self.json()
            items = self.after_get(items)
            return items
        except self.model.DoesNotExist:
            return False

    def insert(self, return_object: bool = False, **kwargs):
        """
        Create a new element in the DB.
        If serializer is provided, it validates the fields against the serializer
        :param return_object: Return Django ORM objects
        :param kwargs: Fields to save in the model
        :return:
        """
        data = self.before_create(kwargs)
        serialize = self._serializer(data=data, context=self._context)
        valid = serialize.is_valid(raise_exception=True)
        if valid:
            data_saved = serialize.save()
            self._results = self.after_created(data_saved)
            if return_object or not self._serializer:
                return data_saved
            return self.json()

    def update_by(self, partial: bool = False, return_object: bool = False, by: str = "id", **kwargs):
        """
        Update an element in the DB.
        If serializer is provided, it validates the fields against the serializer
        :param by: Field by which to update
        :param partial: Allow update certain fields in an elements
        :param return_object: Return Django ORM objects
        :param kwargs: Fields to save in the model
        :return:
        """
        assert by in kwargs, "The field by which it is going to be updated was not defined"
        try:
            id_to_update = {by: kwargs[by]}
            model_object = self.model.objects.get(**id_to_update)
            if f"new_{by}" in kwargs.keys():
                kwargs[by] = kwargs[f"new_{by}"]
                del kwargs[f"new_{by}"]
            serialize = self._serializer(model_object, data=kwargs, partial=partial)
            valid = serialize.is_valid(raise_exception=True)
            if valid:
                data = self.before_update(model_object, kwargs)
                data_saved = serialize.save(**data)
                self._results = self.after_update(data_saved)
                if return_object or not self._serializer:
                    return data_saved
                return self.json()
        except self.model.DoesNotExist:
            return False

    def delete_all(self, soft: bool = True, **kwargs):
        """
        Delete a group of elements in the DB.
        :param soft: Delete or change the elements
        :param kwargs: Filters params to query
        :return:
        """
        models_objects = self.model.objects.filter(**kwargs)
        self.before_delete_all(models_objects)
        if soft:
            for instance in models_objects:
                instance.is_active = False
                instance.deleted = True
                instance.deleted_at = now()
            self.model.objects.bulk_update(
                models_objects, ["is_active", "deleted", "deleted_at"]
            )
        else:
            models_objects.delete()
        self.after_delete_all()
        return True

    def delete_by(self, soft: bool = True, by: str = "id", **kwargs):
        """
        Delete an element in the DB.

        :param by:
        :param soft: Delete or change the element
        :param kwargs: Filters params to query
        :return:
        """
        assert by in kwargs.keys(), "The field by which it is going to be deleted was not defined"
        try:
            id_to_delete = {by: kwargs[by]}
            model_object = self.model.objects.get(**id_to_delete)
            self.before_delete(model_object)
            if soft:
                model_object.deleted_at = now()
                model_object.is_active = False
                model_object.deleted = True
                model_object.save()
            else:
                model_object.delete()
            self.after_delete()
            return True
        except self.model.DoesNotExist:
            return False

    def restore_by(self, **kwargs):
        """
        Restore an element in the DB.
        :param kwargs: Filters params to query
        :return:
        """
        try:
            kwargs["is_active"] = False
            model_object = self.model.objects.get(**kwargs)
            self.before_restore(model_object)
            model_object.is_active = True
            model_object.save()
            self.after_restore()
            return True
        except self.model.DoesNotExist:
            return False

    def restore_all(self, **kwargs):
        """
        Restore a group of elements in the DB.
        :param kwargs: Filters params to query
        :return:
        """
        models_objects_filters = self.model.objects.filter(is_active=False, **kwargs)
        self.before_restore_all(models_objects_filters)

        for model_object in models_objects_filters:
            model_object.is_active = True
        self.model.objects.bulk_update(models_objects_filters, ["is_active"])
        self.after_restore_all()
        return True

    """
    Trigger methods
    """

    def before_get(self):
        pass

    def after_get(self, row):
        return row

    def before_create(self, row):
        return row

    def after_created(self, row):
        return row

    def before_update(self, instance, row):
        return row

    def after_update(self, row):
        return row

    def before_delete(self, row):
        return row

    def after_delete(self):
        pass

    def before_delete_all(self, queryset):
        return queryset

    def after_delete_all(self):
        pass

    def before_restore(self, row):
        pass

    def after_restore(self):
        pass

    def before_restore_all(self, queryset):
        return queryset

    def after_restore_all(self):
        pass

    """
    Output Method
    """

    def get_data(self, data, many=False):
        if self._serializer:
            serializer = self._serializer(data, many=many)
            return serializer.data

    def json(self):
        """
        Convert and return in json the results
        :return: JSON Parseable
        """
        if isinstance(self._results, list) or isinstance(self._results, QuerySet):
            true__data = self._serializer(self._results, many=True, context=self._context).data
            return true__data, self._total
        elif self._serializer:
            return self._serializer(self._results, context=self._context).data
