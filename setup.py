from setuptools import setup


setup(
    version='0.1',
    name='django-enum-field',
    install_requires=[
        'python-enumeration',
        'Django >= 1.8',
    ],
    py_modules=['enum_field'],
)