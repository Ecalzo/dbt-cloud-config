import pytest
from unittest.mock import patch

from src.changelog import create_changelog
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


@patch("src.changelog.get_dbt_project_id", mock_get_dbt_project_id)
def test_create_changelog(configured_jobs, cloud_jobs):
    changelog = create_changelog(cloud_jobs, configured_jobs)
    for k, v in changelog.items():
        assert changelog[k]['diff']['dictionary_item_removed'][0] == "root['project_id']"
        assert changelog[k]['diff']['values_changed'] == {"root['settings']['threads']": {
            'new_value': 4, 'old_value': 5}, "root['schedule']['date']['cron']": {'new_value': '0 1 * * *', 'old_value': '0 2 * * *'}}
