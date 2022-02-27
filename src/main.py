from venv import create
from api import create_or_update_cloud_jobs, list_all_jobs, create_or_update_cloud_jobs
from yaml_parser import get_configured_jobs
from changelog import create_changelog


def main():
    # compare job to config
    # update jobs where applicable
    # create jobs where applicable
    configured_jobs = get_configured_jobs()
    cloud_jobs = list_all_jobs()
    changelog = create_changelog()
    create_or_update_cloud_jobs(changelog)
