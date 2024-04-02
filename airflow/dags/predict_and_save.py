from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 31),
}

dag = DAG('mlflow_example', default_args=default_args, schedule_interval=None)

mlflow_command = "mlflow run /app --env-manager local "

run_mlflow_task = BashOperator(
    task_id='run_mlflow_task',
    bash_command=mlflow_command,
    dag=dag
)

run_mlflow_task
