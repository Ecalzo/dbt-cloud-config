from os.path import exists
from dbtcloudconfig.yaml_parser import read_jobs_yaml, validate_yaml_contents
import yaml
from yaml.loader import SafeLoader
import pytest


def test_config_exists():
    assert exists("./jobs.yml")


def test_read_yaml():
    with open("./jobs.yml", "r") as yml_file:
        assert yaml.load(yml_file, Loader=SafeLoader) == read_jobs_yaml()


@pytest.mark.parametrize("yaml_contents", (
    """jobs:
  - name: some job""",
    """jobs:
  - name: first job
    steps:
      - dbt run
  - name: second job
    steps:"""
))
def test_validate_yaml_contents_keys(yaml_contents):
    data = yaml.load(yaml_contents, Loader=SafeLoader)
    with pytest.raises(KeyError):
        validate_yaml_contents(data)


@pytest.mark.parametrize("yaml_contents", (
    """jobs:
  - name: production job
    description: job that runs our production models
    environment_id: production
    threads: 4
    target_name: prod
    steps:
""",
))
def test_validate_yaml_contents_steps_not_empty(yaml_contents):
    data = yaml.load(yaml_contents, Loader=SafeLoader)
    with pytest.raises(Exception):
        validate_yaml_contents(data)
