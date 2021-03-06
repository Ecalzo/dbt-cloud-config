import os
import pytest
from unittest.mock import patch
from dbtcloudconfig.api import create_or_update_cloud_jobs, get_base_url, get_dbt_api_token, get_dbt_project_id, create_job, update_job


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


@patch("dbtcloudconfig.api.create_job")
@patch("dbtcloudconfig.api.update_job")
def test_create_or_update_cloud_jobs(mock_update_job, mock_create_job, changelog):
    create_or_update_cloud_jobs(changelog)
    assert mock_update_job.called
    update_conf = changelog[list(changelog.keys())[0]]
    assert mock_update_job.calledwith(update_conf)
    assert not mock_create_job.called


@patch("dbtcloudconfig.api.make_post_request")
def test_create_job(mock_make_post_request, changelog):
    job_config = changelog[list(changelog.keys())[0]]
    create_job(job_config)
    assert mock_make_post_request.called


@patch("dbtcloudconfig.api.make_post_request")
def test_update_job(mock_make_post_request, changelog):
    job_config = changelog[list(changelog.keys())[0]]
    update_job(job_config)
    assert mock_make_post_request.called
    call_args = mock_make_post_request.call_args.kwargs
    assert call_args["json_payload"]["id"] is not None
    assert "description" not in call_args["json_payload"]
    assert call_args["url"].endswith("/")
    assert call_args["url"].endswith(call_args["json_payload"]["id"] + "/")
