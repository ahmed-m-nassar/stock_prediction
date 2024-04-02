from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 3, 28),
}

def append_hello_to_file():
    with open("./file.txt", "a") as file:
        file.write("hello " + str(datetime.now()) + "\n")

dag = DAG(
    'dummy_dag',
    default_args=default_args,
    description='A simple dummy DAG',
    schedule_interval=timedelta(minutes=5),
    catchup=False
)

start_task = DummyOperator(task_id='start_task', dag=dag)

append_to_file_task = PythonOperator(
    task_id='append_to_file_task',
    python_callable=append_hello_to_file,
    dag=dag
)

end_task = DummyOperator(task_id='end_task', dag=dag)

start_task >> append_to_file_task >> end_task
