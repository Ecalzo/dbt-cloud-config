import os
import pytest
from unittest.mock import patch
from src.api import create_or_update_cloud_jobs, get_base_url, get_dbt_api_token, get_dbt_project_id, create_job, make_post_request


def test_get_base_url_exception():
    os.environ["DBT_ACCOUNT_ID"] = ""
    with pytest.raises(Exception):
        get_base_url()


def test_get_dbt_api_token_exception():
    os.environ["DBT_API_TOKEN"] = ""
    with pytest.raises(Exception):
        get_dbt_api_token()


def test_get_dbt_project_id_exception():
    os.environ["DBT_PROJECT_ID"] = ""
    with pytest.raises(Exception):
        get_dbt_project_id()


def test_get_base_url():
    dbt_account_id = os.getenv("DBT_ACCOUNT_ID")
    url = f"https://cloud.getdbt.com/api/v2/accounts/{dbt_account_id}/jobs/"
    assert url == get_base_url()


@patch("src.api.create_job")
@patch("src.api.update_job")
def test_create_or_update_cloud_jobs(mock_update_job, mock_create_job, changelog):
    create_or_update_cloud_jobs(changelog)
    assert mock_update_job.called
    for k, v in changelog.items():
        assert mock_update_job.calledwith(v)
    assert not mock_create_job.called


@patch("src.api.make_post_request")
def test_create_job(mock_make_post_request, changelog):
    job_config = changelog[list(changelog.keys())[0]]
    create_job(job_config)
    assert mock_make_post_request.called
