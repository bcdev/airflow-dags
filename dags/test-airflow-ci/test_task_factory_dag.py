from airflow import DAG
from datetime import datetime
from task_factory import task_factory

with DAG(
    dag_id="task_factory_dag_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    task = task_factory(
        task_id="process_data",
        image="syogesh9/test-runner:v1",
        func_path="actual_package.preprocessing.process",
        func_kwargs={
            "data": "iris",
            "transform": "scale_and_rotate",
            "path": "/tmp/iris_output.csv"
        },
        env="prod"
    )