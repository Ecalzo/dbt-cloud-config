import yaml
from yaml.loader import SafeLoader


def read_jobs_yaml():
    with open("./jobs.yml", "r") as yml_file:
        data = yaml.load(yml_file, Loader=SafeLoader)
    return data


def validate_yaml_contents(yaml_contents: dict):
    job_level_keys = [
        "name",
        "description",
        "environment_id",
        "settings",
        "triggers",
        "schedule",
        "execute_steps",
    ]
    try:
        jobs = yaml_contents["jobs"]
    except KeyError:
        raise KeyError("Expected jobs section at top level of jobs.yml")

    for job in jobs:
        for key in job_level_keys:
            if key not in job:
                if key != "name":
                    raise KeyError(f"Expected {key} in {job['name']}")
                else:
                    raise KeyError("Expected name key in job section")
            elif key == "steps" and not job["steps"]:
                job_name = job["name"]
                raise Exception(f"jobs section is empty for job {job_name}")


def get_configured_jobs():
    yaml_data = read_jobs_yaml()
    validate_yaml_contents(yaml_data)
    return yaml_data["jobs"]


if __name__ == "__main__":
    print(read_jobs_yaml())
