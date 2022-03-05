# setup.py for a python package


from setuptools import setup, find_packages


setup(
    name='dbtcloudjobconfig',
    version='0.1',
    description='A library to easily configure dbt Cloud jobs',
    author='Evan Calzolaio',
    entry_points={
        'console_scripts': ['dbtconfig=dbtcloudjobconfig.cli:main'],
    },
    packages=find_packages(),

    install_requires=[
        'requests',
        'deepdiff',
        'pyyaml'
    ]
)
