# setup.py for a python package


from setuptools import setup, find_packages


setup(
    name='dbtcloudconfig',
    version='0.1',
    description='A library to easily configure dbt Cloud jobs',
    author='Evan Calzolaio',
    entry_points={
        'console_scripts': ['dbtconfig=dbtcloudconfig.cli:main'],
    },
    packages=find_packages('src'),
    package_dir={"": "src"},

    install_requires=[
        'requests',
        'deepdiff',
        'pyyaml'
    ]
)
