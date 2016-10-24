from os import environ


def setup():
    environ['DJANGO_SETTINGS_MODULE'] = 'tests.stub_django_project.settings'
