from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sql import SQLExecuteQueryOperator
from airflow.utils.dates import days_ago

def call_script(script, data_type):
    exec(open(script).read(), {'current_day': datetime.now().strftime('%Y-%m-%d'), 'data_type': data_type})

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='gdelt_processing_daily',
    default_args=default_args,
    description='Daily processing of GDELT data',
    schedule_interval='0 1 * * *',  # Daily at 01:00
    start_date=days_ago(1),
    catchup=False,
    tags=['gdelt']
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

extract_exports = PythonOperator(
    task_id='extract_exports',
    python_callable=call_script,
    op_args=['gdelt_extractor.py', 'export'],
    dag=dag
)

extract_mentions = PythonOperator(
    task_id='extract_mentions',
    python_callable=call_script,
    op_args=['gdelt_extractor.py', 'mentions'],
    dag=dag
)

extract_gkg = PythonOperator(
    task_id='extract_gkg',
    python_callable=call_script,
    op_args=['gdelt_extractor.py', 'gkg'],
    dag=dag
)

raw_data_collected = DummyOperator(
    task_id='raw_data_collected',
    dag=dag
)

process_exports = PythonOperator(
    task_id='process_exports',
    python_callable=call_script,
    op_args=['gdelt_processor.py', 'export'],
    dag=dag
)

process_mentions = PythonOperator(
    task_id='process_mentions',
    python_callable=call_script,
    op_args=['gdelt_processor.py', 'mentions'],
    dag=dag
)

process_gkg = PythonOperator(
    task_id='process_gkg',
    python_callable=call_script,
    op_args=['gdelt_processor.py', 'gkg'],
    dag=dag
)

create_datamart = SQLExecuteQueryOperator(
    task_id='create_datamart',
    sql='update_datamart.sql',
    dag=dag
)

finish = DummyOperator(
    task_id='finish',
    dag=dag
)

start >> [extract_exports, extract_mentions, extract_gkg] >> raw_data_collected
raw_data_collected >> [process_exports, process_mentions, process_gkg] >> create_datamart >> finish
