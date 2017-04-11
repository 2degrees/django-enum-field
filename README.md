[![Build Status](https://travis-ci.org/2degrees/django-enum-field.svg?branch=master)](https://travis-ci.org/2degrees/django-enum-field) 
[![Coverage Status](https://coveralls.io/repos/github/2degrees/django-enum-field/badge.svg?branch=master)](https://coveralls.io/github/2degrees/django-enum-field?branch=master)

# django-enum-field

A Django field for use with [python-enumeration](https://github.com/2degrees/python-enumeration).

## Getting started

django-enum-field can be installed from PyPi via:

```bash
pip install django-enum-field
```

## Using in your models

```python
>>> from django.db.models import Model
>>> from enum_field import Enum, EnumField
>>> CLOTHING_SIZES = Enum(
...     ('xs', 'EXTRA_SMALL'),
...     ('s', 'SMALL'),
...     ('m', 'MEDIUM'),
...     ('l', 'LARGE'),
...     ('xl', 'EXTRA_LARGE'),
...     ('xxl', 'EXTRA_EXTRA_LARGE'),
... )
>>> class ClothingItem(Model):
...     size = EnumField(CLOTHING_SIZES)
```

You can now use the enum in your look-ups:

```python
>>> ClothingItem.objects.filter(size=CLOTHING_SIZES.SMALL)
[...]
>>> ClothingItem.objects.filter(size__in=CLOTHING_SIZES.SMALL.subsequent_values)
```

You can set the field value to an enum item:

```python
>>> item = ClothingItem.objects.create(size=CLOTHING_SIZES.LARGE)
```

If you're using Django forms, you can specify UI labels for your enum
and they'll be used in any model forms:

```python
>>> # Before defning the model:
>>> CLOTHING_SIZES.set_ui_labels({
...     CLOTHING_SIZES.EXTRA_SMALL: 'Extra small',
...     CLOTHING_SIZES.SMALL: 'Small',
...     CLOTHING_SIZES.MEDIUM: 'Medium',
...     CLOTHING_SIZES.LARGE: 'Large',
...     CLOTHING_SIZES.EXTRA_LARGE: 'Extra large',
...     CLOTHING_SIZES.EXTRA_EXTRA_LARGE: 'Extra extra large',
... })
>>> ClothingItem._meta.get_field('size').choices
((<EnumItem: value='xs', index=0>, 'Extra small'), (<EnumItem: value='s', index=1>, 'Small'), (<EnumItem: value='m', index=2>, 'Medium'), (<EnumItem: value='l', index=3>, 'Large'), (<EnumItem: value='xl', index=4>, 'Extra large'), (<EnumItem: value='xxl', index=5>, 'Extra extra large'))
>>> # If you're not using ModelForm, but want the choices:
>>> CLOTHING_SIZES.get_ui_labels()
((<EnumItem: value='xs', index=0>, 'Extra small'), (<EnumItem: value='s', index=1>, 'Small'), (<EnumItem: value='m', index=2>, 'Medium'), (<EnumItem: value='l', index=3>, 'Large'), (<EnumItem: value='xl', index=4>, 'Extra large'), (<EnumItem: value='xxl', index=5>, 'Extra extra large'))
```

## Migrations

`EnumField` is full deconstructible and is, therefore, compatible with 
Django's migration system. **Please note**, to make the underlying `Enum`
and `EnumItem` compatible with Django's migration system, you _must_
use the sub-classes available from `enum_field.Enum` and 
`enum_field.EnumItem` and *not* from the `python-enumeration` project.


# Changelog

## Version 1.0 Beta 1 (unreleased)

- Fell back to using the enum values in the field `choices` if the UI labels
  are not set.
- **Backwardly incompatible:** Dropped ability to set custom field choices.
