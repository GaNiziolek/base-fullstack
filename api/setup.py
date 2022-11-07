from importlib.metadata import entry_points
from pkg_resources import require
from setuptools import setup

requires = [
    'waitress',
    'cornice',
    'sqlalchemy'
]

setup(
    name    = 'api',
    version = '0.0.1',
    install_requires = requires,
    entry_points= {
        'paste.app_factory': [
            'main = api:main'
        ]
    }
)