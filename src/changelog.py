# flow will be
# list current jobs
# compare job names to see what to update
# if something has changed, update the entire job
# how to diff check?
from src.api import get_dbt_project_id

from deepdiff import DeepDiff
from collections import defaultdict


def create_changelog(cloud_jobs, configured_jobs):
    if not cloud_jobs:
        return []
    current_proj_jobs = [
        job for job in cloud_jobs if job["project_id"] == get_dbt_project_id()
    ]
    diff = compare_jobs(current_proj_jobs, configured_jobs)
    return diff


def create_changelog_mapping(current_project_jobs, configured_jobs):
    change_map = defaultdict(dict)
    for cloud_job in current_project_jobs:
        change_map[cloud_job["name"]]["existing"] = cloud_job
        change_map[cloud_job["name"]]["mode"] = "update"

    for config_job in configured_jobs:
        if config_job["name"] not in change_map:
            # if there is no existing version of this conf, set create mode
            change_map[config_job["name"]]["existing"] = {}
            change_map[config_job["name"]]["mode"] = "create"
        change_map[config_job["name"]]["configured"] = config_job
    return change_map


def compare_jobs(current_jobs, configured_jobs):
    job_map = defaultdict(dict)
    for cloud_job in current_jobs:
        job_map[cloud_job["name"]]["existing"] = cloud_job
        job_map[cloud_job["name"]]["mode"] = "update"

    for config_job in configured_jobs:
        if config_job["name"] not in job_map:
            # if there is no existing version of this conf, set create mode
            job_map[config_job["name"]]["existing"] = {}
            job_map[config_job["name"]]["mode"] = "create"
        job_map[config_job["name"]]["configured"] = config_job

    cloud_only_jobs = []
    for job_name, job_meta in job_map.items():
        # handle jobs that are only confgured in the cloud
        configured = job_meta.get("configured", None)
        if configured is None:
            cloud_only_jobs.append(job_name)
            continue
        diff = DeepDiff(job_meta["existing"], configured)
        print(diff)
        job_map[job_name]["diff"] = diff

    return job_map
