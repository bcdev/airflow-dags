from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import \
    KubernetesPodOperator

with DAG(
    'first_mlflow_dag',
    schedule_interval=None,
) as dag:
    task1 = KubernetesPodOperator(
        task_id='ml_test_task',
        name='ml_test-pod',
        image='syogesh9/airflow-dags-ml-test:v7',
        cmds=['python', '-m', 'ml_test'],
        dag=dag,
        log_events_on_failure=True,
        get_logs=True,
    )