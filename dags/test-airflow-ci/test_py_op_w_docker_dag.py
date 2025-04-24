from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
import json

def create_kpo_task(task_id, image, function_path, function_kwargs):
    return KubernetesPodOperator(
        task_id=task_id,
        name=task_id,
        image=image,
        cmds=["python", "runner.py"],
        env_vars={
            "FUNC_PATH": function_path,
            "FUNC_KWARGS": json.dumps(function_kwargs)
        },
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
        do_xcom_push=True
    )

with DAG(
    dag_id="kpo_ml_task_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    task = create_kpo_task(
        task_id="process_data",
        image="syogesh9/kpo-test:v6",
        function_path="actual_package.preprocessing.process",
        function_kwargs={
            "data": "iris",
            "transform": "scale_and_rotate",
            "path": "/tmp/iris_output.csv"
        }
    )
