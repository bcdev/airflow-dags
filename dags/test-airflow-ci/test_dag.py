from _datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import \
    KubernetesPodOperator

with DAG(
    'first_test_dag',
    schedule_interval=None,
    start_date=datetime(2025,4,22),
) as dag:
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

    task3 = KubernetesPodOperator(
        task_id='task3',
        name='task3-pod',
        image='syogesh9/airflow-dags-test:v6',
        cmds=['python', '-m', 'task3'],
        dag=dag,
        log_events_on_failure=True,
        get_logs=True,
    )

task1 >> task2 >> task3