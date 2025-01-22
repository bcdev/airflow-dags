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
        image='syogesh9/airflow-dags-test:latest',
        cmds=['python', '-m', 'scripts.task1'],
        namespace='airflow-dag-test',
        dag=dag,
    )

    task2 = KubernetesPodOperator(
        task_id='task2',
        name='task2-pod',
        image='syogesh9/airflow-dags-test:latest',
        cmds=['python', '-m', 'scripts.task2'],
        namespace='airflow-dag-test',
        dag=dag,
    )

    task3 = KubernetesPodOperator(
        task_id='task3',
        name='task3-pod',
        image='syogesh9/airflow-dags-test:latest',
        cmds=['python', '-m', 'scripts.task3'],
        namespace='airflow-dag-test',
        dag=dag,
    )

task1 >> task2 >> task3