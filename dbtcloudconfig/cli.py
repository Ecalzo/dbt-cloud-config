from dbtcloudconfig.api import create_or_update_cloud_jobs, list_all_jobs
from dbtcloudconfig.changelog import create_changelog
from dbtcloudconfig.yaml_parser import get_configured_jobs


def main():
    configured_jobs = get_configured_jobs()
    cloud_jobs = list_all_jobs()
    changelog = create_changelog(cloud_jobs, configured_jobs)
    create_or_update_cloud_jobs(changelog)
