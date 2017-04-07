# -*- coding: utf-8 -*-
from nose.tools import assert_raises
from nose.tools import eq_
from nose.tools import ok_

from enum_field import Enum, EnumItem, EnumField, EnumFieldValidationError


class TestEnumDjangoSpecifics(object):
    """Tests for :class:`Enum`."""

    def setup(self):
        self.enum_args = ('stop', 'STOP'), ('go', 'GO')
        self.enum = Enum(*self.enum_args)

    def test_enum_is_deconstruction(self):
        ok_(hasattr(self.enum, 'deconstruct'))
        enum_deconstructed = self.enum.deconstruct()
        class_name, args, kwargs = enum_deconstructed
        eq_('enum_field.Enum', class_name)
        eq_(self.enum_args, args)
        eq_({}, kwargs)

    def test_enum_item_is_deconstruction(self):
        enum_item = self.enum.STOP
        ok_(hasattr(enum_item, 'deconstruct'))
        enum_item_deconstructed = enum_item.deconstruct()
        class_name, args, kwargs = enum_item_deconstructed
        eq_('enum_field.EnumItem', class_name)
        enum_item_values = list(zip(*self.enum_args))[0]
        eq_((enum_item.item_value, enum_item_values), args)
        eq_({}, kwargs)


class TestEnumField(object):
    """Tests for :class:`EnumField`."""

    def setup(self):
        self.CLOTHES_SIZE_ENUM = Enum(
            ('xs', 'EXTRA_SMALL'),
            ('s', 'SMALL'),
            ('m', 'MEDIUM'),
            ('l', 'LARGE'),
            ('xl', 'EXTRA_LARGE'),
            ('xxl', 'EXTRA_EXTRA_LARGE'),
        )

        self.enum_field = EnumField(self.CLOTHES_SIZE_ENUM)

        self.items_ui_labels = {
            self.CLOTHES_SIZE_ENUM.EXTRA_SMALL: 'Extra small',
            self.CLOTHES_SIZE_ENUM.SMALL: 'Small',
            self.CLOTHES_SIZE_ENUM.MEDIUM: 'Medium',
            self.CLOTHES_SIZE_ENUM.LARGE: 'Large',
            self.CLOTHES_SIZE_ENUM.EXTRA_LARGE: 'Extra large',
            self.CLOTHES_SIZE_ENUM.EXTRA_EXTRA_LARGE: 'Extra extra large',
        }

    def test_max_length(self):
        """The field takes its maximum length from the longest enum value."""
        enum_field = EnumField(self.CLOTHES_SIZE_ENUM)

        eq_(enum_field.max_length, 3)

    def test_conversion_from_string_to_python(self):
        """The field is converted to an Enum item if it's set as a string."""

        eq_(self.CLOTHES_SIZE_ENUM.EXTRA_SMALL, self.enum_field.to_python('xs'))

        with assert_raises(EnumFieldValidationError) as context_manager:
            self.enum_field.to_python('ultra_large')
        exception = context_manager.exception
        eq_("'ultra_large' must be a value in the enum", exception.message)
        eq_('cannot_resolve_item', exception.code)

    def test_conversion_from_enum_item_to_python(self):
        """The field is left as is if it's set as an enum item."""

        eq_(
            self.CLOTHES_SIZE_ENUM.EXTRA_SMALL,
            self.enum_field.to_python(self.CLOTHES_SIZE_ENUM.EXTRA_SMALL),
        )

        enum_item = EnumItem('baby', ('baby', 'adult'))
        with assert_raises(EnumFieldValidationError) as context_manager:
            self.enum_field.to_python(enum_item)
        exception = context_manager.exception
        eq_(
            'Enum item {!r} does not belong to this enum'.format(enum_item),
            exception.message,
        )
        eq_('does_not_belong', exception.code)

    def test_conversion_from_none_to_python(self):
        eq_(None, self.enum_field.to_python(None))

    def test_get_prep_value(self):
        eq_('s', self.enum_field.get_prep_value(self.CLOTHES_SIZE_ENUM.SMALL))

    def test_get_prep_value_calls_to_python(self):
        with assert_raises(EnumFieldValidationError):
            self.enum_field.get_prep_value('xxs')

    def test_get_prep_value_with_none(self):
        eq_(None, self.enum_field.get_prep_value(None))

    def test_from_db_value(self):
        enum_value = self.enum_field.from_db_value('s', None, None, None)
        eq_(self.CLOTHES_SIZE_ENUM.SMALL, enum_value)

    def test_from_db_value_with_none(self):
        enum_value = self.enum_field.from_db_value(None, None, None, None)
        eq_(None, enum_value)

    def test_enum_with_ui_labels(self):
        self.CLOTHES_SIZE_ENUM.set_ui_labels(self.items_ui_labels)

        enum_field = EnumField(self.CLOTHES_SIZE_ENUM)

        eq_(enum_field.choices, self.CLOTHES_SIZE_ENUM.get_ui_labels())

    def test_enum_without_ui_labels(self):
        enum_items_by_values = self.CLOTHES_SIZE_ENUM.get_items_by_values()
        expected_choices = [(i, v) for v, i in enum_items_by_values.items()]
        eq_(expected_choices, self.enum_field.choices)

    def test_custom_choices(self):
        with assert_raises(TypeError):
            EnumField(
                self.CLOTHES_SIZE_ENUM,
                choices=(('a', 'Apple'), ('b', 'Ball')),
            )

    def test_deconstruction(self):
        field_deconstructed = self.enum_field.deconstruct()
        _, class_name, args, kwargs = field_deconstructed

        eq_('enum_field.EnumField', class_name)
        eq_(1, len(args))
        eq_(self.enum_field.enum, args[0])
        eq_(0, len(kwargs))


CLOTHING_SIZES = Enum(
    ('xs', 'EXTRA_SMALL'),
    ('s', 'SMALL'),
    ('m', 'MEDIUM'),
    ('l', 'LARGE'),
    ('xl', 'EXTRA_LARGE'),
    ('xxl', 'EXTRA_EXTRA_LARGE'),
)
CLOTHING_SIZES.set_ui_labels({
    CLOTHING_SIZES.EXTRA_SMALL: 'Extra small',
    CLOTHING_SIZES.SMALL: 'Small',
    CLOTHING_SIZES.MEDIUM: 'Medium',
    CLOTHING_SIZES.LARGE: 'Large',
    CLOTHING_SIZES.EXTRA_LARGE: 'Extra large',
    CLOTHING_SIZES.EXTRA_EXTRA_LARGE: 'Extra extra large',
})
