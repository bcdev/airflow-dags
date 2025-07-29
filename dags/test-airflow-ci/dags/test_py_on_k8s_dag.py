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
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            image="docker.io/syogesh9/hello-world:v1",
                        )
                    ]
                )
            )
        },
    )

    task1