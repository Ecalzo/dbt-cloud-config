from dbtcloudjobconfig.api import create_or_update_cloud_jobs, list_all_jobs, create_or_update_cloud_jobs
from dbtcloudjobconfig.yaml_parser import get_configured_jobs
from dbtcloudjobconfig.changelog import create_changelog


def main():
    configured_jobs = get_configured_jobs()
    cloud_jobs = list_all_jobs()
    changelog = create_changelog(cloud_jobs, configured_jobs)
    import pdb
    pdb.set_trace()
    create_or_update_cloud_jobs(changelog)


if __name__ == "__main__":
    main()
