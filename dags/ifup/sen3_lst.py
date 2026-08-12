"""Nightly Sentinel-3 land-surface-temperature processing."""

from datetime import UTC, datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s


with DAG(
    dag_id="ifup_sen3_lst",
    description="Fetch and append Sentinel-3 land-surface-temperature data.",
    start_date=datetime(2024, 1, 1, tzinfo=UTC),
    schedule="0 3 * * *",
    catchup=False,
    max_active_runs=1,
    is_paused_upon_creation=True,
    params={
        "bbox": Param(
            default=[6.5, 51.0, 7.0, 51.5],
            type="array",
            items={"type": "number"},
            minItems=4,
            maxItems=4,
            description="[west, south, east, north] in EPSG:4326.",
        ),
        "time_range": Param(
            default=None,
            type=["null", "array"],
            items={"type": "string", "format": "date"},
            minItems=2,
            maxItems=2,
            description=(
                "Optional [start, end] override in YYYY-MM-DD format. "
                "If omitted, the DAG uses its Airflow data interval."
            ),
        ),
    },
) as dag:
    KubernetesPodOperator(
        task_id="run_pipeline",
        name="ifup-sen3-lst",
        image="docker.io/fredsdev/ifup:0.1.3",
        cmds=["/opt/ifup/entrypoint.sh", "ifup"],
        arguments=[
            "run",
            "sen3_lst",
            "--params-json",
            """{
                \"bbox\": {{ params.bbox | tojson }},
                \"time_range\": {{ (params.time_range or [
                    (data_interval_start or logical_date.subtract(days=1)).strftime(\"%Y-%m-%d\"),
                    (data_interval_end or logical_date).strftime(\"%Y-%m-%d\"),
                ]) | tojson }}
            }""",
        ],
        namespace="ifup",
        env_from=[
            k8s.V1EnvFromSource(
                secret_ref=k8s.V1SecretEnvSource(name="ifup-secrets")
            )
        ],
        in_cluster=True,
        get_logs=True,
        is_delete_operator_pod=True,
    )
