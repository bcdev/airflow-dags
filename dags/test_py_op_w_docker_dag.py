from airflow.decorators import dag, task
from datetime import datetime
from kubernetes.client import models as k8s
from airflow.operators.python import PythonOperator


executor_config = {
    "pod_override": k8s.V1Pod(
        spec=k8s.V1PodSpec(
            containers=[
                k8s.V1Container(
                    name="base",
                    image="syogesh9/airflow-dags-ml-test:v8",
                )
            ]
        )
    )
}

@dag(
    schedule_interval=None,
    start_date=datetime(2025, 4, 22),
    catchup=False,
    tags=["example"],
)
def my_custom_dag():
    from ml_test import run
    t1 = PythonOperator(
        task_id='run_ml_test_from_docker_using_py_o',
        python_callable=run,
        executor_config=executor_config,
    )

    t1

my_custom_dag()
