from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.utils.deconstruct import deconstructible
from enumeration import Enum as PythonEnum
from enumeration import EnumItem as PythonEnumItem


class EnumField(CharField):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        self.enum_items_by_values = enum.get_items_by_values()

        if enum.has_ui_labels:
            choices = enum.get_ui_labels()
        else:
            choices = [(i, v) for v, i in self.enum_items_by_values.items()]

        longest_enum_value = max(len(enum_value) for enum_value in enum)
        super(EnumField, self).__init__(
            max_length=longest_enum_value,
            choices=choices,
            *args,
            **kwargs
        )

    def deconstruct(self):
        name, path, args, kwargs = super(EnumField, self).deconstruct()
        args.insert(0, self.enum)
        del kwargs['choices']
        del kwargs['max_length']
        return name, path, args, kwargs

    def to_python(self, value):
        enum_item = coerce_value_to_enum_item(self.enum, value)
        return enum_item

    def from_db_value(self, value, expression, connection, context):
        value = self.to_python(value)
        return value

    def get_prep_value(self, value):
        if value is not None:
            value = str(self.to_python(value))
        return value


@deconstructible
class EnumItem(PythonEnumItem):
    pass


@deconstructible
class Enum(PythonEnum):
    item_class = EnumItem


class EnumFieldValidationError(ValidationError):
    pass


def coerce_value_to_enum_item(enum, value):
    enum_items_by_values = enum.get_items_by_values()

    if isinstance(value, EnumItem):
        enum_values = list(enum_items_by_values.keys())
        if list(value.enum_values) != enum_values:
            raise EnumFieldValidationError(
                'Enum item {!r} does not belong to this enum'.format(value),
                code='does_not_belong',
            )

        enum_item = value

    elif value is None:
        enum_item = value

    else:
        if value not in enum_items_by_values:
            raise EnumFieldValidationError(
                '{!r} must be a value in the enum'.format(value),
                code='cannot_resolve_item',
            )
        enum_item = enum_items_by_values[value]

    return enum_item
