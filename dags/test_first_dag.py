from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import \
    KubernetesPodOperator

with DAG(
    'first_test_dag',
    schedule_interval=None,
) as dag:
    task1 = KubernetesPodOperator(
        task_id='task1',
        name='task1-pod',
        image='syogesh9/airflow-dags-test:v1',
        cmds=['python', '-m', 'task1'],
        dag=dag,
        log_events_on_failure=True,
        get_logs=True,
        do_xcom_push=False,
        in_cluster=True,
        namespace='airflow',
        is_delete_operator_pod=False
    )

    task2 = KubernetesPodOperator(
        task_id='task2',
        name='task2-pod',
        image='syogesh9/airflow-dags-test:v1',
        cmds=['python', '-m', 'task2'],
        dag=dag,
    )

    task3 = KubernetesPodOperator(
        task_id='task3',
        name='task3-pod',
        image='syogesh9/airflow-dags-test:v1',
        cmds=['python', '-m', 'task3'],
        dag=dag,
    )

task1 >> task2 >> task3