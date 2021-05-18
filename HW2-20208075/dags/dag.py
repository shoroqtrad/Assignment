import json
from datetime import timedelta
from airflow.utils.dates import days_ago
import logging
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
#pip3 install_pymongo

LOGGER = logging.getLogger("Airflow_TASK")

default_args = {
    'owner': 'Shrouq_Al-Fuqahaa',
    'depends_on_past': False,
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
        'GAG_HW2',
        default_args=default_args,
        schedule_interval=None,
        start_date=days_ago(3),
        tags=['ETL'],
) as dag:
    def ID_generator(**kwargs):
        import uuid
        id = uuid.uuid4()
        LOGGER.info('ID' + str(id))
        ti = kwargs['ti']
        ti.xcom_push(key='file_id', value=str(id))

    def Json2Mongo(**kwargs):
        ti = kwargs['ti']
        id = ti.xcom_pull(key='file_id', task_ids=['generate_id'])[0]

        from pymongo import MongoClient

        client = MongoClient("mongodb://mongoadmin:mongo@de_mongo:27017")

        db = client["HW2"]

        Collection = db["table1"]

        # Loading or Opening the json file
        with open('/home/airflow/data/' + str(id) + '.json') as file:
            file_data = json.load(file)
            Collection.insert_many(file_data)

     def converter(**kwargs):
        ti = kwargs['ti']
        id = ti.xcom_pull(key='file_id', task_ids=['generate_id'])[0]
        df = pd.read_csv('/home/airflow/data/' + str(id) + '.csv')
        df.reset_index(inplace=True)
        dict = df.to_dict("Rcords
        LOGGER.info(str(dict))
        with open('/home/airflow/data/' + str(id) + '.json', 'w') as file:
            json.dump(dict, file)
        LOGGER.info('convert to json ')
    ID_generator= PythonOperator(
        task_id='ID_generator',
        python_callable=ID_generator,
        provide_context=True,
        dag=dag,
    )

    getCSV = BashOperator(
        task_id='getCSV',
        bash_command='psql postgresql://postgres:postgres@de_postgres:5432 -c "\copy table1 to \'/home/airflow/data/{{ti.xcom_pull(key="file_id", task_ids=["generate_id"])[0]}}.csv\' csv header ;"',
        dag=dag
    )
    converter = PythonOperator(
        task_id='converter',
        python_callable=converter,
        provide_context=True,
        dag=dag,
    )
    Json2Mongo = PythonOperator(
        task_id='Json2Mongo',
        python_callable=Json2Mongo,
        provide_context=True,
        dag=dag
    )
    ID_generator >> getCSV>> converter >> Json2Mongo
