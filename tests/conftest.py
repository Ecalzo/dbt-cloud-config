import pytest
import os

from dbtcloudconfig.yaml_parser import get_configured_jobs
from dbtcloudconfig.changelog import create_changelog


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
    base_jobs[0]["id"] = "1234"
    return base_jobs


@pytest.fixture
def changelog(configured_jobs, cloud_jobs):
    return create_changelog(cloud_jobs, configured_jobs)
