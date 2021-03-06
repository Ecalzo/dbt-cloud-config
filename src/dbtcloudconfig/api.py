import os

import requests


def get_dbt_api_token():
    dbt_api_token = os.getenv("DBT_API_TOKEN")
    if not dbt_api_token:
        raise Exception("expected environment variable DBT_API_TOKEN")
    return dbt_api_token


def get_dbt_project_id():
    dbt_project_id = os.getenv("DBT_PROJECT_ID")
    if not dbt_project_id:
        raise Exception("expected environment variable DBT_PROJECT_ID")
    return int(dbt_project_id)


def get_dbt_account_id():
    dbt_account_id = os.getenv("DBT_ACCOUNT_ID")
    if not dbt_account_id:
        raise Exception("expected environment variable DBT_ACCOUNT_ID")
    return int(dbt_account_id)


def get_base_url():
    dbt_account_id = get_dbt_account_id()
    url = f"https://cloud.getdbt.com/api/v2/accounts/{dbt_account_id}/jobs/"
    return url


def list_all_jobs():
    dbt_api_token = get_dbt_api_token()
    base_url = get_base_url()

    headers = {"Accept": "application/json", "Authorization": f"Token {dbt_api_token}"}
    return requests.get(base_url, headers=headers).json()["data"]


def create_or_update_cloud_jobs(changelog):
    for job_name, job_meta in changelog.items():
        if job_meta["mode"] == "create":
            create_job(job_meta["configured"])
        if job_meta["mode"] == "update":
            if job_meta.get("configured", None):
                update_job(job_meta)


def make_post_request(url, json_payload):
    dbt_api_token = get_dbt_api_token()
    headers = {"Accept": "application/json", "Authorization": f"Token {dbt_api_token}"}
    return requests.post(url=url, headers=headers, json=json_payload)


def update_job(job_meta):
    base_url = get_base_url()
    existing_config = job_meta["existing"]
    job_config = job_meta["configured"]
    # append the job id that we want to update
    base_url += str(existing_config["id"]) + "/"
    payload = get_base_payload()
    for key, value in job_config.items():
        if key != "description":
            payload[key] = value
    payload["schedule"]["time"] = {"type": "every_hour", "interval": 1}
    payload["id"] = existing_config["id"]
    response = make_post_request(url=base_url, json_payload=payload)
    response.raise_for_status()
    print(response.text)


def create_job(job_config):
    base_url = get_base_url()
    payload = get_base_payload()
    for key, value in job_config.items():
        if key != "description":
            payload[key] = value
    payload["schedule"]["time"] = {"type": "every_hour", "interval": 1}
    response = make_post_request(url=base_url, json_payload=payload)
    response.raise_for_status()
    print(response.text)


def get_base_payload():
    dbt_account_id = get_dbt_account_id()
    dbt_project_id = get_dbt_project_id()
    payload = {
        "id": None,  # required due to api bug
        "account_id": dbt_account_id,
        "project_id": dbt_project_id,
        "environment_id": None,
        "name": None,
        "execute_steps": None,
        "dbt_version": None,  # use environment's
        "triggers": {
            "github_webhook": False,
            "schedule": True,
            "custom_branch_only": False,
        },
        "settings": {"threads": 4, "target_name": "prod"},
        "state": 1,
        "generate_docs": False,
        "schedule": {
            "date": {"type": "custom_cron", "cron": None},
            # this does not actually do anyting, but we have to leave it for the api to behave
            "time": {"type": "every_hour", "interval": 1},
        },
    }
    return payload


if __name__ == "__main__":
    print(list_all_jobs())
