from setuptools import setup, find_packages
import sys, os

version = '0.0'

requires = (
    'nextgisweb',
    'geojson',
    'sqlalchemy',
    'geoalchemy',
    'requests',
    'psycopg2',
    'argparse',
)

entry_points = {
    'nextgisweb.packages': ['nextgisweb_entels = nextgisweb_entels:pkginfo', ],
    'nextgisweb.amd_packages': [
        'nextgisweb_entels = nextgisweb_entels:amd_packages',
    ],
}

setup(
    name='nextgisweb_entels',
    version=version,
    description='nextgisweb_entels',
    long_description="NextGIS Web module for Entels",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    keywords='info@nextgis.ru',
    author='NextGIS',
    author_email='http://nextgis.com/',
    url='https://github.com/nextgis/nextgisweb_entels',
    license='GNU GPL v2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points=entry_points,
)
