from _datetime import datetime
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.providers.cncf.kubernetes.operators.pod import \
    KubernetesPodOperator

with DAG(
    'example_kpo_dag',
    description="A simple example KPO DAG",
    schedule=None,
    start_date=datetime(2025,4,22),
    tags=["example"]
) as dag:
    with TaskGroup(group_id="Group_1",
                   tooltip="Change what appears in the tooltip") as tg1:
        task1 = KubernetesPodOperator(
            task_id='task1',
            name='task1-pod',
            image='syogesh9/airflow-dags-test:v6',
            cmds=['/opt/conda/bin/python', '-m', 'task1'],
            dag=dag,
            log_events_on_failure=True,
            get_logs=True,
        )

        task2 = KubernetesPodOperator(
            task_id='task2',
            name='task2-pod',
            image='syogesh9/airflow-dags-test:v6',
            cmds=['python', '-m', 'task2'],
            dag=dag,
            log_events_on_failure=True,
            get_logs=True,
        )

        task1 >> task2

    task3 = KubernetesPodOperator(
        task_id='task3',
        name='task3-pod',
        image='syogesh9/airflow-dags-test:v6',
        cmds=['python', '-m', 'task3'],
        dag=dag,
        log_events_on_failure=True,
        get_logs=True,
    )

    task4 = KubernetesPodOperator(
        task_id="ml_test_task",
        name="ml_test-pod",
        image="syogesh9/airflow-dags-ml-test:v7",
        cmds=["python", "-m", "ml_test"],
        dag=dag,
        log_events_on_failure=True,
        get_logs=True,
    )

tg1 >> task3
tg1 >> task4