# flow will be
# list current jobs
# compare job names to see what to update
# if something has changed, update the entire job
# how to diff check?
from .api import list_all_jobs, get_dbt_project_id
from .yaml_parser import read_jobs_yaml


def create_changelog():
    all_jobs = list_all_jobs()
    if not all_jobs:
        return []
    current_proj_jobs = [
        job for job in all_jobs if job["project_id"] == get_dbt_project_id()
    ]
    configured_jobs = read_jobs_yaml()
    diff = compare_jobs(current_proj_jobs, configured_jobs)


def compare_jobs(current_jobs, configured_jobs):
    current_jobs.sort(key=lambda x: x["name"])
    configured_jobs.sort(key=lambda x: x["name"])
