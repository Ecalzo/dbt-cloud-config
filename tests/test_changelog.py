from unittest.mock import patch
from deepdiff.diff import DeepDiff

from dbtcloudconfig.changelog import create_changelog, create_changelog_mapping, compare_jobs
from tests.conftest import mock_get_dbt_project_id


def test_create_changelog(configured_jobs, cloud_jobs):
    changelog = create_changelog(cloud_jobs, configured_jobs)
    for k, v in changelog.items():
        assert changelog[k]['diff']['dictionary_item_removed'][0] == "root['project_id']"
        assert changelog[k]['diff']['values_changed'] == {"root['settings']['threads']": {
            'new_value': 4, 'old_value': 5}, "root['schedule']['date']['cron']": {'new_value': '0 1 * * *', 'old_value': '0 2 * * *'}}


def test_create_changelog_mapping(configured_jobs, cloud_jobs):
    change_map = create_changelog_mapping(cloud_jobs, configured_jobs)
    for k, v in change_map.items():
        assert "existing" in change_map[k]
        assert "mode" in change_map[k]
        assert "configured" in change_map[k]


def test_create_changelog_mapping_with_empty_cloud_jobs(configured_jobs):
    change_map = create_changelog_mapping([], configured_jobs)
    first_item = change_map[list(change_map.keys())[0]]
    assert "existing" in first_item
    assert "mode" in first_item
    assert "configured" in first_item


def test_compare_jobs(configured_jobs, cloud_jobs):
    change_map = compare_jobs(cloud_jobs, configured_jobs)
    for k, v in change_map.items():
        assert "diff" in v
        assert type(v["diff"]) == DeepDiff
