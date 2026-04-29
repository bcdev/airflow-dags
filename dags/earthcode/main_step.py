# WARNING - THIS IS GENERATED CODE
#   Generator: Eozilla Appligator v0.1.0.dev0
#        Date: 2026-04-01T14:10:33.403138

import json
from datetime import datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s


with DAG(
    dag_id="main_step",
    start_date=datetime.fromisoformat("2026-03-31"),
    schedule=None,
    catchup=False,
    is_paused_upon_creation=False,
    params={
    "start_date": Param(type='string', title='Start date.', format='date'),
    "end_date": Param(type='string', title='End date.', format='date'),
    "bbox": Param(default=[-180, -90, 180, 90], type=['null', 'array'], title='Bounding box as [west, south, east, north] in EPSG:4326.', format='bbox', items={'type': 'number'}),
    "output_prefix": Param(default='smos-sm/global', type='string', title='S3 output prefix.', description="Key prefix under which staging and ARD Zarr stores are written. Defaults to 'smos-sm/global' for production runs."),
    "stac_s3_bucket": Param(default=None, type=['null', 'string'], title='STAC catalog S3 bucket.', description="S3 bucket for the STAC catalog and deep-code user storage. Defaults to the ARD cube bucket when not set.")
    },
) as dag:

    tasks = {}


    tasks["main_step"] = KubernetesPodOperator(
        task_id="main_step",
        image="quay.io/earthcode/smos-ard-pipeline:0.0.6",
        cmds=["python", "/opt/pixi/run_step.py"],
        arguments=[json.dumps({
            "func_module": "smos_ard.workflow",
            "func_qualname": "pipeline_params",
            "inputs": {"start_date": "{{ params.start_date }}",
"end_date": "{{ params.end_date }}",
"bbox": "{{ params.bbox }}",
"output_prefix": "{{ params.output_prefix }}",
"stac_s3_bucket": "{{ params.stac_s3_bucket }}"},
            "output_keys": ['start_date', 'end_date', 'bbox', 'output_prefix', 'stac_s3_bucket'],
        })],
        namespace="earthcode",
        env_from=[k8s.V1EnvFromSource(secret_ref=k8s.V1SecretEnvSource(name='earthcode-secrets'))],
        do_xcom_push=True,
    )


    tasks["fetch_data"] = KubernetesPodOperator(
        task_id="fetch_data",
        image="quay.io/earthcode/smos-ard-pipeline:0.0.6",
        cmds=["python", "/opt/pixi/run_step.py"],
        arguments=[json.dumps({
            "func_module": "smos_ard.workflow",
            "func_qualname": "fetch_data",
            "inputs": {"start_date": "{{ ti.xcom_pull(task_ids='main_step')['start_date'] }}",
"end_date": "{{ ti.xcom_pull(task_ids='main_step')['end_date'] }}",
"bbox": "{{ ti.xcom_pull(task_ids='main_step')['bbox'] }}",
"output_prefix": "{{ ti.xcom_pull(task_ids='main_step')['output_prefix'] }}"},
            "output_keys": ['return_value'],
        })],
        namespace="earthcode",
        env_from=[k8s.V1EnvFromSource(secret_ref=k8s.V1SecretEnvSource(name='earthcode-secrets'))],
        do_xcom_push=True,
    )


    tasks["aggregate_data"] = KubernetesPodOperator(
        task_id="aggregate_data",
        image="quay.io/earthcode/smos-ard-pipeline:0.0.6",
        cmds=["python", "/opt/pixi/run_step.py"],
        arguments=[json.dumps({
            "func_module": "smos_ard.workflow",
            "func_qualname": "aggregate_data",
            "inputs": {"fetch_result": "{{ ti.xcom_pull(task_ids='fetch_data')['return_value'] }}"},
            "output_keys": ['return_value'],
        })],
        namespace="earthcode",
        env_from=[k8s.V1EnvFromSource(secret_ref=k8s.V1SecretEnvSource(name='earthcode-secrets'))],
        do_xcom_push=True,
    )


    tasks["publish_data"] = KubernetesPodOperator(
        task_id="publish_data",
        image="quay.io/earthcode/smos-ard-pipeline:0.0.6",
        cmds=["python", "/opt/pixi/run_step.py"],
        arguments=[json.dumps({
            "func_module": "smos_ard.workflow",
            "func_qualname": "publish_data",
            "inputs": {"agg_result": "{{ ti.xcom_pull(task_ids='aggregate_data')['return_value'] }}",
"stac_s3_bucket": "{{ ti.xcom_pull(task_ids='main_step')['stac_s3_bucket'] }}"},
            "output_keys": ['return_value'],
        })],
        namespace="earthcode",
        env_from=[k8s.V1EnvFromSource(secret_ref=k8s.V1SecretEnvSource(name='earthcode-secrets'))],
        do_xcom_push=True,
    )


    def _final_step_callable(ti, upstream_task_id):
        return ti.xcom_pull(task_ids=upstream_task_id)
    
    tasks["__procodile_final_step__"] = PythonOperator(
        task_id="__procodile_final_step__",
        python_callable=_final_step_callable,
        op_kwargs={
            "upstream_task_id": "publish_data"
        },
        do_xcom_push=True
    )

    tasks["main_step"] >> tasks["fetch_data"]
    tasks["fetch_data"] >> tasks["aggregate_data"]
    tasks["aggregate_data"] >> tasks["publish_data"]
    tasks["publish_data"] >> tasks["__procodile_final_step__"]

