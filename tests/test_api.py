import os
import pytest
from src.api import get_base_url, get_dbt_api_token, get_dbt_project_id


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
