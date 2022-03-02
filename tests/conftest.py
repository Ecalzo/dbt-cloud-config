import pytest
import os

from src.yaml_parser import get_configured_jobs
from src.changelog import create_changelog


def mock_get_dbt_project_id():
    return 100


@pytest.fixture(autouse=True)
def set_env_variables():
    os.environ["DBT_ACCOUNT_ID"] = "48682"
    os.environ["DBT_PROJECT_ID"] = "100"
    os.environ["DBT_API_TOKEN"] = "asdfsdf32423423"


@pytest.fixture
def configured_jobs():
    return get_configured_jobs()


@pytest.fixture
def cloud_jobs():
    base_jobs = get_configured_jobs()
    # alter some of the config values
    base_jobs[0]["settings"]["threads"] = 5
    base_jobs[0]["schedule"]["date"]["cron"] = "0 2 * * *"
    base_jobs[0]["project_id"] = mock_get_dbt_project_id()
    return base_jobs
