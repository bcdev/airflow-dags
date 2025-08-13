from _datetime import datetime

from airflow import DAG
from kubernetes.client import models as k8s, V1EnvVar
from airflow.operators.python import PythonOperator


def task1():
    print("Hello world from dag file!!!")

with DAG(
    'test_python_op_on_k8sexec',
    schedule_interval=None,
    start_date=datetime(2025,4,22),
) as dag:
    task1 = PythonOperator(
        task_id="task1",
        python_callable=task1,
        executor_config={
            "KubernetesExecutor": {
                "image": "346516713328.dkr.ecr.eu-central-1.amazonaws.com/tac:0.0.1"
            }
        },
    )

    task1