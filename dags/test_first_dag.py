from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.task1 import task1_function
from scripts.task2 import task2_function
from scripts.task3 import task3_function

with DAG(
    'first_test_dag',
    schedule_interval=None,
) as dag:

    task1 = PythonOperator(
        task_id='task1',
        python_callable=task1_function,
        dag=dag,
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=task2_function,
        dag=dag,
    )

    task3 = PythonOperator(
        task_id='task3',
        python_callable=task3_function,
        dag=dag,
    )

    task1 >> task2 >> task3