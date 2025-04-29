from airflow import DAG
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from task_factory import task_factory
with DAG(
    dag_id="task_factory_dag_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    preprocess = task_factory(
        task_id="preprocess_data",
        image="syogesh9/cc-cm-package:v1",
        func_path="tac.preprocess",
        func_kwargs={
            "path": "/tmp/iris_output.csv"
        },
        env="prod"
    )

    train = task_factory(
        task_id="train",
        image="syogesh9/cc-cm-package:v1",
        func_path="tac.train",
        xcom_pull_tasks={
            "preprocessed_path": {"task": "preprocess_data", "key": "preprocessed_data_path"}
        },
        env="prod"
    )

    preprocess >> train