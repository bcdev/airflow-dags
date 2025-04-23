from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from datetime import datetime

def print_msg(msg, **context):
    print(msg)
    return msg.upper()

with (DAG('xcom_demo', start_date=datetime(2025,4,22), schedule_interval=None)
      as dag):
    t1 = PythonOperator(
        task_id='print_hello',
        python_callable=print_msg,
        op_kwargs={'msg': 'hello from PythonOperator - Test'}
    )

    @task
    def flow_task():
        return "hello from TaskFlow"

    t2 = flow_task()

    def consume(**context):
        val1 = context['ti'].xcom_pull(task_ids='print_hello')
        val2 = context['ti'].xcom_pull(task_ids='flow_task')
        print(f"Values: {val1}, {val2}")

    t3 = PythonOperator(
        task_id='consume_xcom',
        python_callable=consume
    )

    t1 >> t3
    t2 >> t3
