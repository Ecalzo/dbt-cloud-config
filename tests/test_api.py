import os
import pytest
from src.api import get_base_url, get_dbt_api_token, get_dbt_project_id


def test_get_base_url_exception():
    with pytest.raises(Exception):
        get_base_url()


def test_get_dbt_api_token_exception():
    with pytest.raises(Exception):
        get_dbt_api_token()


def test_get_dbt_project_id_exception():
    with pytest.raises(Exception):
        get_dbt_project_id()


def test_get_base_url():
    dbt_account_id = "48682"
    os.environ["DBT_ACCOUNT_ID"] = dbt_account_id
    url = f"https://cloud.getdbt.com/api/v2/accounts/{dbt_account_id}/jobs/"
    assert url == get_base_url()
