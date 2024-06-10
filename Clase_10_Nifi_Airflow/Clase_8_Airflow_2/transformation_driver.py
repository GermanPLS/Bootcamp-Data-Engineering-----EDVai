rom datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='example-DAG',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
    tags=['ingest', 'transform'],
    params={"example_key": "example_value"},
) as dag:

    comienza_proceso = DummyOperator(
        task_id='comenzar_proceso',
    )


    ingest = BashOperator(
        task_id='ingest',
        bash_command='sshpass -p "edvai" ssh hadoop@172.18.0.8 /usr/bin/sh /home/hadoop/scripts/formula.sh ',
    )


    transform = BashOperator(
        task_id='transform',
        bash_command='sshpass -p "edvai" ssh hadoop@172.18.0.8 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/scripts/transformation_driver.py ',
    )

 finaliza_proceso = DummyOperator(
        task_id='finalizar_proceso',
    )

    comienza_proceso >> ingest >> transform >>finaliza_proceso




if __name__ == "__main__":
    dag.cli()