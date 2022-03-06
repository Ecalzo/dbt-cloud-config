# dbt Cloud Config

configuration as code for dbt jobs

## Getting Started

the `dbtconfig` command expects a `jobs.yml` in the current directory.

```shell
$ python setup.py install
$ export DBT_API_TOKEN = <token>
$ export DBT_PROJECT_ID = <project_id>
$ export DBT_ACCOUNT_ID = <account_id>
$ dbtconfig
```

## Configuring Jobs

This library does not make any assumptions about configured jobs, therefore
all of the items you see in the `jobs.yml` file are required. This is in part because of restrictions imposed by the current state of the [dbt Cloud v2 API](https://docs.getdbt.com/dbt-cloud/api-v2). For example, the API requires all values to be sent in a POST request, though not explicitly stated in the documentation.

```yaml
jobs:
  - name: production job
    description: job that runs our production models
    environment_id: 68525
    settings:
      threads: 4
      target_name: prod
    triggers:
      github_webhook: False
      schedule: True
      custom_branch_only: False
    schedule:
      date:
        type: custom_cron
        cron: 0 1 * * *
    execute_steps:
      - dbt run
      - dbt test
    generate_docs: False
```

## Roadmap

Roadmap is in order of importance

1. Dry-run capability
2. Distribute to pypi
3. Improve information-level logging
4. Report what updated/changed in a more human-readable format
5. Better GitHub action integration
