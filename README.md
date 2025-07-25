# CDR (Centralized DAG Repository)

This repository acts as the **central source of truth for DAGs** developed 
across various projects at BC. 

## Purpose

- **Centralized Management**: Hosts and manages all production-ready Airflow 
DAGs.
- **Repository Dispatch Trigger**: Listens for [repository dispatch events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch) 
from other repositories to dynamically sync relevant DAGs.
- **S3 Integration**: Pulls DAGs from a configured S3 bucket based on 
dispatch payload.
- **Airflow Sync**: Git-synced with the **Airflow production server running 
in Kubernetes**, ensuring that the latest DAGs are always available and deployed.

## Architecture Overview

1. Other repositories trigger a `repository_dispatch` event when a new DAG or 
DAG update is ready - this happens during a Github release.
2. This repository receives the dispatch, fetches the DAG(s) from a specified
S3 bucket.
3. DAGs are placed in the `dags` folder, committed and pushed.
4. `GitSync` propagates the change to the Airflow production server running 
in a Kubernetes pod.

## Requirements

- An `S3 bucket` with DAGs stored in project-specific paths.
- A `GitHub personal access token` with workflow and repository access for 
allowing the Git bit to push to this repository.
- A `Github actions ECR Role` to assume so that the CI can authenticate to the AWS.
- Kubernetes-deployed `Airflow setup with DAG GitSync` enabled.

## Relevant Links

- [Airflow `GitSync` Documentation](https://airflow.apache.org/docs/helm-chart/1.5.0/manage-dags-files.html#mounting-dags-from-a-private-github-repo-using-git-sync-sidecar)
- [GitHub `repository_dispatch` event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch)
