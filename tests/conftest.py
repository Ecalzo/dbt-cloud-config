import pytest
from src.yaml_parser import get_configured_jobs


def mock_get_dbt_project_id():
    return 100


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
